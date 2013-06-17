#!/bin/bash
./_commit.sh $@ && ./_push.sh $@ && ./_sync_web.sh
