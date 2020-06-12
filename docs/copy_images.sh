echo "Copying images"

mkdir build
mkdir build/html
mkdir build/html/tutorials
mkdir build/html/tutorials/formatter
mkdir build/html/tutorials/formatter/formatter_pdf_images
mkdir build/html/tutorials/formatter/formatter_html_images
mkdir build/html/tutorials/formatter/tutorials
mkdir build/html/tutorials/formatter/tutorials/formatter
mkdir build/html/tutorials/formatter/tutorials/formatter/formatter_pdf_images
mkdir build/html/tutorials/formatter/tutorials/formatter/formatter_html_images
#
#mkdir html/
#mkdir html/tutorials
#mkdir html/tutorials/formatter
#mkdir html/tutorials/formatter/tutorials
#mkdir html/tutorials/formatter/tutorials/formatter
#mkdir html/tutorials/formatter/tutorials/formatter/formatter_pdf_images
#mkdir html/tutorials/formatter/tutorials/formatter/formatter_html_images

cp -a ../tutorials/formatter/portable_document/formatter_pdf_images/. build/html/tutorials/formatter/tutorials/formatter/formatter_pdf_images/
cp -a ../tutorials/formatter/hypertext_markup/formatter_html_images/. build/html/tutorials/formatter/tutorials/formatter/formatter_html_images/
cp -a ../tutorials/formatter/portable_document/formatter_pdf_images/. build/html/tutorials/formatter/formatter_pdf_images/
cp -a ../tutorials/formatter/hypertext_markup/formatter_html_images/. build/html/tutorials/formatter/formatter_html_images/
#cp -a ../tutorials/formatter/portable_document/formatter_pdf_images/. html/tutorials/formatter/tutorials/formatter/formatter_pdf_images/
#cp -a ../tutorials/formatter/hypertext_markup/formatter_html_images/. html/tutorials/formatter/tutorials/formatter/formatter_html_images/
