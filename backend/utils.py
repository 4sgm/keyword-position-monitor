from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

def normalize_url(u: str) -> str:
    """Normalize a URL for matching: lowercase host, strip utm params, fragment, default ports, trailing slash nuances."""
    if not u:
        return u
    try:
        p = urlparse(u.strip())
        query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if not k.lower().startswith("utm_")]
        # Remove gclid and common tracking params
        query = [(k, v) for (k, v) in query if k.lower() not in {"gclid","fbclid","msclkid"}]
        netloc = p.netloc.lower()
        # Remove default ports
        if netloc.endswith(":80"):
            netloc = netloc[:-3]
        if netloc.endswith(":443"):
            netloc = netloc[:-4]
        # Remove trailing slash from path unless root
        path = p.path or "/"
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        return urlunparse((p.scheme.lower() if p.scheme else "https", netloc, path, "", urlencode(query), ""))
    except Exception:
        return u.strip().lower()

def urls_match(target: str, candidate: str) -> bool:
    """Domain-level match: candidate domain must be same as target domain, path can vary.
    We match by netloc primarily; if path present on target, require candidate to start with that path.
    """
    t = urlparse(normalize_url(target))
    c = urlparse(normalize_url(candidate))
    if t.netloc != c.netloc:
        return False
    # if target has a path beyond '/', require startswith
    if t.path and t.path != "/":
        return c.path.startswith(t.path)
    return True