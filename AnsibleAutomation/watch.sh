#!/bin/bash
watch -n 20 ssh $1 kubectl get pods -A
