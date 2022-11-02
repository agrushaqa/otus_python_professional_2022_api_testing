import hashlib
import json

from loguru import logger


def get_score(store, phone, email, birthday=None, gender=None, first_name=None,
              last_name=None):
    key_parts = [
        first_name or "",
        last_name or "",
        phone or "",
        birthday.strftime("%Y%m%d") if birthday is not None else "",
    ]
    logger.debug("key_parts:")
    logger.debug(key_parts)
    key = "uid:" + hashlib.md5("".join(key_parts).encode('utf-8')).hexdigest()
    logger.debug("key:")
    logger.debug(key)
    # try get from cache,
    # fallback to heavy calculation in case of cache miss
    score = float(store.cache_get(key) or 0)
    if score:
        return score
    if phone:
        score += 1.5
    if email:
        score += 1.5
    if birthday and gender:
        score += 1.5
    if first_name and last_name:
        score += 0.5
    # cache for 60 minutes
    store.cache_set(key, score, 60 * 60)
    return score


def get_interests(store, cid):
    logger.info(f"get store for: i:{cid}'")
    r = store.get(f"i:{cid}")
    return json.loads(r) if r else []
