from elasticsearch_dsl import connections, Index, Document
from elasticsearch import Elasticsearch, helpers

conn = connections.create_connection(alias='default', hosts=['128.0.255.6'], timeout=20)


def main():
    import time
    start = time.time()
    index_name = 'test_index'
    es_index = Index(index_name)
    if not es_index.exists():
        es_index.put_alias(using='default')
        # Number of data node
        es_index.settings(number_of_shards=1)
        es_index.save()
    else:
        es_index.put_alias(using='default', name="sss3")
    doc = Document(first_name='cheng', last_name="unknowname", hometown='China')
    doc.save(using='default', index=index_name)
    print(time.time() - start)


def add_many():
    import time
    start = time.time()

    def generate_data():
        for i in range(150000):
            data = dict(
                _index="siss",
                first_name="cheng{}".format(i),
                last_name="jianneng{}".format(i),
                hometown="china"
            )
            yield data
    es = Elasticsearch(hosts=['128.0.255.6'])
    helpers.bulk(es, generate_data())
    print(time.time() - start)


if __name__ == '__main__':
    main()
    # add_many()
