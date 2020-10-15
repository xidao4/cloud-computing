package producer;

import java.util.HashMap;
import java.util.Map;

public class Response {
    private boolean success=false;
    private Map<String,String> resultMap=new HashMap<>();

    public boolean isSuccess() {
        return success;
    }

    void setSuccess(boolean success) {
        this.success = success;
    }

    void putResult(String name,String value){
        this.resultMap.put(name,value);
    }

    public String getResult(String name){
        return this.resultMap.getOrDefault(name, null);
    }
}
