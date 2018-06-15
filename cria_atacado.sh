while read CLIENTE
do
  COD_CLI=`echo $CLIENTE | cut -d';' -f1`
  NOM_CLI=`echo $CLIENTE | cut -d';' -f2`
  EST_CLI=`echo $CLIENTE | cut -d';' -f3`
  TIP_CLI=`echo $CLIENTE | cut -d';' -f4`
  echo $COD_CLI":"$NOM_CLI
  echo ${EST_CLI}"_"${TIP_CLI}
  NOME_SEM_DESC="PED_"${EST_CLI}"_"${TIP_CLI}"_SEM_DESC.json"
  NOME_COM_DESC="PED_"${EST_CLI}"_"${TIP_CLI}"_COM_DESC.json"
  ./cria_json_todos_produtos.sh ${COD_CLI} > ./pedidos/$NOME_SEM_DESC
  ./cria_json_todos_com_desconto.sh ${COD_CLI} > ./pedidos/$NOME_COM_DESC
done < clientes_teste.csv
