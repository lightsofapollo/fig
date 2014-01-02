echo "---
layout: default
title: Fig | Punctual, lightweight development environments using Docker
---
" > index.md

git --no-pager show master:README.md >> index.md
