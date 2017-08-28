#!/bin/bash

# crontab: 

ssh matt@the-cluster.org "cd worldpaint/devops_hexaloop && make backup-db"
rsync -avz matt@the-cluster.org:worldpaint/devops_hexaloop/dump_* .
