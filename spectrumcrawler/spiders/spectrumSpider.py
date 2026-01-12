import scrapy
from scrapy.exceptions import CloseSpider
import re


class SpectrumSpider(scrapy.Spider):
    name = "spectrumSpider"

    # Allow both
    allowed_domains = ["library.concordia.ca", "spectrum.library.concordia.ca"]

    # Start from Spectrum home
    start_urls = ["https://spectrum.library.concordia.ca/"]

    def __init__(self, limit=300, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.max_thesis_pdfs = int(limit)
        except (TypeError, ValueError):
            self.max_thesis_pdfs = 300

        # Track visited HTML pages and unique PDF "logical" URLs
        self.visited_pages = set()
        self.thesis_pdfs = set()

        self.logger.info(f"DEBUG: max_thesis_pdfs = {self.max_thesis_pdfs}")

    # ---------- Helper: normalize PDF URLs ----------
    def normalize_pdf_url(self, url: str) -> str:
        """
        Turn many different PDF URLs of the same thesis into ONE canonical key.
        Examples:
          https://spectrum.library.concordia.ca/995716/1/Azzizi_MCompSC_F2025.pdf
          https://spectrum.library.concordia.ca/995716/2/whatever.pdf?download=1
          https://spectrum.library.concordia.ca/id/eprint/995716/1/file.pdf
          https://spectrum.library.concordia.ca/id/eprint/995716/
        all become:
          https://spectrum.library.concordia.ca/id/eprint/995716/
        """
        if not url:
            return ""

        # Drop fragment and query
        url = url.split("#", 1)[0].split("?", 1)[0].strip()

        # Match either:
        #   https://spectrum.library.concordia.ca/id/eprint/<id>/...
        #   https://spectrum.library.concordia.ca/<id>/...
        m = re.match(
            r"https://spectrum\.library\.concordia\.ca/(?:id/eprint/)?(\d+)",
            url,
        )
        if m:
            thesis_id = m.group(1)
            return f"https://spectrum.library.concordia.ca/id/eprint/{thesis_id}/"

        # Otherwise, just return cleaned URL
        return url

    # ---------- 1) GENERAL PAGES ----------
    def parse(self, response):
        # Stop everything if we already have enough PDFs
        if len(self.thesis_pdfs) >= self.max_thesis_pdfs:
            raise CloseSpider(reason="enough_thesis_pdfs")

        # Only process HTML pages
        content_type = response.headers.get(b"Content-Type", b"").decode("latin1").lower()
        if "html" not in content_type:
            return

        # Normalize current page URL for visited tracking (avoid /x and /x/)
        current_url = response.url.split("#", 1)[0].split("?", 1)[0]
        if current_url in self.visited_pages:
            return
        self.visited_pages.add(current_url)

        # Look at all links on this HTML page
        for href in response.css("a::attr(href)").getall():
            if len(self.thesis_pdfs) >= self.max_thesis_pdfs:
                raise CloseSpider(reason="enough_thesis_pdfs")

            full_url = response.urljoin(href)

            # Only stay on Spectrum subdomain
            if not full_url.startswith("https://spectrum.library.concordia.ca/"):
                continue

            # CASE A: a record page (/id/eprint/...)
            if "/id/eprint/" in full_url:
                record_url = full_url.split("#", 1)[0].split("?", 1)[0]
                if record_url not in self.visited_pages:
                    yield scrapy.Request(record_url, callback=self.parse_record)

            # CASE B: another Spectrum HTML page to explore (year list, division, etc.)
            else:
                # We'll check visited_pages again inside the callback
                yield scrapy.Request(full_url, callback=self.parse)

    # ---------- 2) RECORD PAGES ----------
    def parse_record(self, response):
        """
        Called on individual record pages (/id/eprint/...).
        We collect *all* PDFs (theses + other documents) and keep
        doc_type / thesis_type as metadata.
        """
        # Stop everything if we already have enough
        if len(self.thesis_pdfs) >= self.max_thesis_pdfs:
            raise CloseSpider(reason="enough_thesis_pdfs")

        # Skip non-HTML just in case
        content_type = response.headers.get(b"Content-Type", b"").decode("latin1").lower()
        if "html" not in content_type:
            return

        # Normalize record URL for visited tracking
        record_url = response.url.split("#", 1)[0].split("?", 1)[0]
        self.visited_pages.add(record_url)

        # Read metadata (for theses this will be filled, for others maybe empty)
        doc_type = (response.css('meta[name="eprints.document_type"]::attr(content)').get() or "").lower()
        thesis_type = (response.css('meta[name="eprints.thesis_type"]::attr(content)').get() or "").lower()

        # Collect all PDFs linked from this record page
        for href in response.css("a::attr(href)").getall():
            if len(self.thesis_pdfs) >= self.max_thesis_pdfs:
                raise CloseSpider(reason="enough_thesis_pdfs")

            full_url = response.urljoin(href)

            # Only keep PDFs hosted on Spectrum
            if not (full_url.lower().endswith(".pdf")
                    and full_url.startswith("https://spectrum.library.concordia.ca/")):
                continue

            # --- 1) Use normalized key ONLY for dedup ---
            canonical_key = self.normalize_pdf_url(full_url)

            if canonical_key in self.thesis_pdfs:
                continue

            # Mark this thesis as seen
            self.thesis_pdfs.add(canonical_key)

            # --- 2) Log using canonical key ---
            self.logger.info(
                f"[PDF {len(self.thesis_pdfs)}] {canonical_key} "
                f"(doc_type={doc_type}, thesis_type={thesis_type})"
            )

            # --- 3) Store the REAL .pdf URL in the JSON ---
            yield {
                "thesis_record": record_url,   # /id/eprint/... page (HTML)
                "pdf_url": full_url,          # REAL .pdf link (ends with .pdf)
                "doc_type": doc_type,
                "thesis_type": thesis_type,
            }

            if len(self.thesis_pdfs) >= self.max_thesis_pdfs:
                self.logger.info("Reached max_thesis_pdfs, closing spider now.")
                raise CloseSpider(reason="enough_thesis_pdfs")
