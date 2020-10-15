package producer;

import config.ProducerConfig;
import model.DataModel;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;

import java.util.Properties;
import java.util.concurrent.ExecutionException;

public class MessageProducer {
    private Producer<String, DataModel> producer;
    private static MessageList messageList=MessageList.getInstance();
    public MessageProducer(){
        Properties props = new Properties();
        props.put("bootstrap.servers", config.ProducerConfig.SERVER_ADDRESS);
        props.put("key.serializer", config.ProducerConfig.KEY_SERIALIZER);
        props.put("value.serializer", ProducerConfig.VALUE_SERIALIZER);

        props.put("acks", config.ProducerConfig.ACK);
        props.put("retries", config.ProducerConfig.RETRIES);
        props.put("batch.size", config.ProducerConfig.BATCH_SIZE);
        props.put("linger.ms", config.ProducerConfig.LINGER_MS);
        props.put("buffer.memory", config.ProducerConfig.BUFFER_MEMORY);
        producer=new KafkaProducer<String, DataModel>(props);
    }
    /*
     * 同步发送消息,返回结果
     */
    public Response sendMessageSync(Message message)  {
        String topic=message.getTopic();
        ProducerRecord<String, DataModel> record=
                new ProducerRecord<>(topic,
                        topic.concat("_").concat(String.valueOf(MessageProducer.messageList.getMessageNum(message.getTopic()))),
                        message.getValue());
        Response response=new Response();
        try {
            RecordMetadata result = producer.send(record).get();
            response.setSuccess(true);
            response.putResult("partition", String.valueOf(result.partition()));
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
            response.setSuccess(false);
        }
        return response;
    }
}
