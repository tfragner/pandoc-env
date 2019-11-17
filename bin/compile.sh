HOME=$PWD

rm temp.md book.txt int.md total.md total2.md

find $1 -name "*.md" -type f -not -path "./.pandoc/*" -not -path "./node_modules/*" -not -name "_index.md" | sort > book.txt

FIRST_FILE=true

while read p; do
    echo $p
    FILEPATH=$(pwd)/$p
    DIR=$(dirname "${FILEPATH}")
    if [ "$FIRST_FILE" = true ] ; then
        pandoc "$p" -o int.md \
            --filter pandoc-include-frontmatter.py \
            --atx-headers \
            -s
        cat int.md > total.md
        echo "" >> total.md
        FIRST_FILE=false
    else
        pandoc "$p" --filter pandoc-include-frontmatter.py -o int.md -s --atx-headers -M document-format=content
        pandoc int.md --filter panflute -o int.md --atx-headers -M document-format=content -M filepath=$DIR
        cat int.md >> total.md
        echo "" >> total.md
    fi
done <book.txt

pandoc total.md  -o total2.md --filter panflute -s --atx-headers -M filepath=$HOME --columns 180
pandoc total2.md --filter pandoc-crossref --filter pandoc-citeproc --filter pandoc-alert-boxes.py  --template eisvogel -o result_01.pdf --pdf-engine=xelatex --number-sections -M listings:true --listings  -M crossrefYaml="./.pandoc/includes/pandoc-crossref.yml" -M link-citations -M reference-section-title=Literaturverzeichnis -V geometry:right=3cm -V geometry:left=2.5cm -V geometry:top=2.0cm -V geometry:bottom=2.5cm -M book:true

mkdir _build
mv result_01.pdf _build/$2
rm temp.md book.txt int.md total.md total2.md
