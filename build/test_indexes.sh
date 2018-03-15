idx_types="ef single uniform opt block_optpfor block_varint block_interpolative block_mixed"
query_types="or_freq:maxscore:maxscore_dyn"


COLLECTION_NAME="clueweb_collection"
QUERY_FILEPREFIX="queries"


construct_indexes=false

if [ ! -d ./indexes ] 
then
    mkdir -p ./indexes
fi


if [ ! -d ./query_logs ] 
then
    mkdir -p ./query_logs
fi

./create_wand_data ../test/test_data/$COLLECTION_NAME indexes/$COLLECTION_NAME.wand
for idx in $idx_types; do
    #if [ "$contruct_indexes" =  true ] ; then
        ./create_freq_index $idx ../test/test_data/$COLLECTION_NAME indexes/$COLLECTION_NAME.index.$idx --check
    #fi
    ./queries $idx $query_types indexes/$COLLECTION_NAME.index.$idx indexes/$COLLECTION_NAME.wand < ../test/test_data/$QUERY_FILEPREFIX.txt > query_logs/query_log_$COLLECTION_NAME.$idx.$QUERY_FILEPREFIX
done



