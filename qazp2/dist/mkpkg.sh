WERSJA='qazp2-'$1'.zip'
echo $WERSJA
rm -r qazp2
rm qazp2.zip
rm $WERSJA
mkdir -p qazp2/keza
mkdir qazp2/dane
mkdir qazp2/lib
mkdir -p qazp2/widok/qtqube/pyqube
cp -r ../src/forms qazp2/
cp -r ../src/keza/*.txt qazp2/keza
cp ../src/dane/*.py qazp2/dane/
cp ../src/lib/*.py qazp2/lib
cp ../src/widok/*.py qazp2/widok
cp ../src/widok/qtqube/*.py qazp2/widok/qtqube
cp ../src/widok/qtqube/pyqube/*.py qazp2/widok/qtqube/pyqube
cp ../src/__init__.py qazp2/
cp ../src/qazp.py qazp2/
cp ../src/metadata.txt qazp2/
#cp -r ../src qazp2
#rm qazp2/uruchom.py
zip -r $WERSJA qazp2
cp $WERSJA qazp2.zip
