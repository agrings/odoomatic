COD_CLI=$1
cat templates/inicio.json |sed "s/XXXXX/${COD_CLI}/g"
csva -r itens_pedido_todos.cyx  | grep '<' | sed '$ s/.$//' | sed 's/</[/g;s/>/]/g;s/\./\,/g;s/"0,00/"10,00/g'
cat templates/final.json
rm itens_pedido_todos.csv
