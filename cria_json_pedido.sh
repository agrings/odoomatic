NUM_PED=$1
NUM_PED_SB=`echo ${NUM_PED}| sed 's/\///g'`
COD_CLI=`csva -r odoo_pedido.cyx -p${NUM_PED} |grep '>'|sed 's/>;//g'`
cat templates/inicio.json |sed "s/XXXXX/${COD_CLI}/g"
csva -r odoo_itens_pedido.cyx  -p${NUM_PED}| grep '<' | sed 's/</[/g;s/>/]/g;s/\./\,/g'
cat templates/final.json
