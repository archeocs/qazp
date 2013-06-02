WERSJA='qazp2-'$1'.zip'
echo $WERSJA
rm -r qazp2
rm qazp2.zip
mkdir qazp2
mkdir qazp2/dane
mkdir qazp2/lib
mkdir qazp2/widok
cp -r ../src/forms qazp2/
cp -r ../src/keza qazp2/
cp ../src/dane/*.py qazp2/dane/
cp ../src/lib/*.py qazp2/lib
cp ../src/widok/*.py qazp2/widok
cp ../src/__init__.py qazp2/
cp ../src/qazp.py qazp2/
#cp -r ../src qazp2
#rm qazp2/uruchom.py
zip -r $WERSJA qazp2
cp $WERSJA qazp2.zip
