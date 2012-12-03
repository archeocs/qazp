WERSJA='qazp2-'$1'.zip'
echo $WERSJA
rm -r qazp2
rm qazp2.zip
cp -r ../src qazp2
zip -r $WERSJA qazp2
cp $WERSJA qazp2.zip
