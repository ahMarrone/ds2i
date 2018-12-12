idx_types="opt"
query_types="ranked_or:maxscore:maxscore_smart_dyn"


COLLECTION_NAME=$1 # ej "test_collection" - coleccion .docs .freqs .sizes
QUERY_FILEPREFIX=$2 # ej "queries_test_collection"


construct_indexes=$3

if [ ! -d ./indexes ] 
then
    mkdir -p ./indexes
fi


if [ ! -d ./query_logs ] 
then
    mkdir -p ./query_logs
fi
#if [ "$contruct_indexes" =  true ] ; then
    #./create_wand_data ../test/test_data/$COLLECTION_NAME indexes/$COLLECTION_NAME.wand
#fi
for idx in $idx_types; do
    #if [ "$contruct_indexes" =  true ] ; then
        #./create_freq_index $idx ../test/test_data/$COLLECTION_NAME indexes/$COLLECTION_NAME.index.$idx --check
    #fi
    ./queries $idx $query_types indexes/$COLLECTION_NAME.index.$idx indexes/$COLLECTION_NAME.wand < ../test/test_data/$QUERY_FILEPREFIX.txt > query_logs/query_log_$COLLECTION_NAME.$idx.$QUERY_FILEPREFIX
done




