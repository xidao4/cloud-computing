package producer;

import model.DataModel;

public class Message {
    private String topic=null;
    private DataModel value=null;

    String getTopic() {
        return topic;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    DataModel getValue() {
        return value;
    }

    public void setValue(DataModel value) {
        this.value = value;
    }
}
