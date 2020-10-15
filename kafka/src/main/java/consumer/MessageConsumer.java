package consumer;

import config.ConsumerConfig;
import model.DataModel;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.util.Arrays;
import java.util.Properties;

public class MessageConsumer {
    private Consumer<String, DataModel> consumer;
    private Thread thread;//consumer thread

    public MessageConsumer() {
        Properties props=new Properties();
        props.put("bootstrap.servers", ConsumerConfig.SERVER_ADDRESS);
        props.put("key.deserializer", ConsumerConfig.KEY_DESERIALIZER);
        props.put("value.deserializer", ConsumerConfig.VALUE_DESERIALIZER);

        props.put("group.id", ConsumerConfig.GROUP_ID);
        props.put("enable.auto.commit", ConsumerConfig.ENABLE_AUTO_COMMIT);
        props.put("auto.commit.interval.ms", ConsumerConfig.AUTO_COMMIT_INTERVAL);
        consumer=new KafkaConsumer<String, DataModel>(props);
    }

    public void subscribeTopics(String... args){ this.consumer.subscribe(Arrays.asList(args)); }

    public void consumeMessage(){
        MessageConsumer that=this;
        Thread t=new Thread(new Runnable() {
            @Override
            public void run() {
                //auto-offset-commit
                while(true){
                    ConsumerRecords<String,DataModel> records=consumer.poll(100);
                    for(ConsumerRecord<String,DataModel> record:records){
                        System.out.println("offset="+record.offset()+ ", key="+record.key());
                        System.out.println("record="+record.value().toString());
                    }
                }
            }
        });
        that.thread=t;
        t.start();
    }
}
