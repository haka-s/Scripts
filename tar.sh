#!/bin/bash
op=$(find *.tar.gz)
for line in $op
do
        ((i=i+1))
        echo $i")" $line
done

IFS=$'\n';  arrIN=($op);unset IFS

read -p 'seleccione un archivo ' tare
((tarex = $tare - 1))

read -p 'extension of the compressed file: ' filetype

files=$(tar -ztvf "${arrIN[$tarex]}" --wildcards "*.$filetype" | cut -d " " -f 6)
if [[ -z $files ]]
then
        echo "no se encontraron archivos"
else
        for file in $files
        do
                tar -zxvf "${arrIN[$tarex]}" --transform='s/.*\///' -C $(pwd) $file
        done
find $(pwd) -type d -empty -delete
fi
exit
