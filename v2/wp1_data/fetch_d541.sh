#!/bin/bash
# Fetch the 5 DANDI sessions with resume and retries.  truncation self-heals because each file is
# re-tried until its size matches the target.
while IFS=$'\t' read -r sub url sz; do
  [ -z "$sub" ] && continue
  out="/tmp/d541/$sub.nwb"
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    cur=$(stat -f%z "$out" 2>/dev/null || echo 0)
    if [ "$cur" -ge "$sz" ]; then echo "  $sub 完整 ($((cur/1000000)) MB)"; break; fi
    echo "  $sub 尝试 $attempt: $((cur/1000000))/$((sz/1000000)) MB"
    curl -sL -C - --max-time 900 --retry 5 --retry-delay 3 --retry-all-errors "$url" -o "$out" || true
    sleep 3
  done
  cur=$(stat -f%z "$out" 2>/dev/null || echo 0)
  [ "$cur" -ge "$sz" ] && echo "  $sub DONE" || echo "  $sub INCOMPLETE $((cur/1000000))/$((sz/1000000)) MB"
done < /tmp/dl_urls2.txt
echo "ALL DONE"
