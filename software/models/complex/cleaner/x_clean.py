#!/bin/bash

for i in *; do
    if ! grep -qxFe "$i" dont_delete.txt; then
        echo "Deleting: $i"
        # the next line is commented out.  Test it.  Then uncomment to removed the files
        #read -p "Are you sure? " -n 1 -r
        #echo    # (optional) move to a new line
        #if [[ ! $REPLY =~ ^[Yy]$ ]]
        #then
        #    exit 1
        #fi
        
        
        rm -R  "$i"
    fi
done
