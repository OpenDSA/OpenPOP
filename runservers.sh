#!/bin/bash

bundle exec thin start --ssl --ssl-key-file server.key --ssl-cert-file server.crt -p 9295
