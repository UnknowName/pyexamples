# 注意点

   因为`Kafka`自动创建`topic`时存在一个过程与时间。`aiokafka`的`provider`直接发数据时，第一条会失败。
   
   因此，在启动时，需要先启动`consumer`。 `consumer`在监听`topic`时也会导致`kafka`自动创建`topic` 