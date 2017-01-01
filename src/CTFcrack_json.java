import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.*;
import org.json.JSONObject;
import com.google.gson.*;
import com.google.gson.reflect.TypeToken;
public class CTFcrack_json{
	//Json解析
	public String getDetail(String title) throws Exception{
	    // 创建json解析器
	    JsonParser parser = new JsonParser(); 
	    // 使用解析器解析json数据，返回值是JsonElement，强制转化为其子类JsonObject类型
	    JsonObject object =  (JsonObject) parser.parse(new FileReader(System.getProperty("user.dir")+"\\Setting.json"));
	    // 使用JsonObject的get(String memeberName)方法返回JsonElement，再使用JsonElement的getAsXXX方法得到真实类型
	    // 遍历JSON数组
	    String detailStr=null;
	    JsonArray Plugins = object.getAsJsonArray("Plugins");
	    for (JsonElement jsonElement : Plugins) {
	        JsonObject Plugin = jsonElement.getAsJsonObject();
	        if(Plugin.get("title").getAsString().equalsIgnoreCase(title)){
	        	detailStr = "<html>"
	        				+ "插件名："+Plugin.get("title").getAsString()+"<br/>"
	        				+"作者："+Plugin.get("autor").getAsString()+"<br/>"
	        				+"插件详情："+Plugin.get("detail").getAsString()+"<br/>"
	        				+"插件地址："+Plugin.get("path").getAsString()
	        				+ "</html>";
	        }
	    }
	    return detailStr;
	}
	//Json写入
	public void createJSON(String path) throws IOException{
		File file = new File(path);
		String title=null,type=null,autor=null,detail=null;
	    try{
	    	InputStreamReader readpy = new InputStreamReader(new FileInputStream(file));
	    	BufferedReader pyPluginread = new BufferedReader(readpy);
	    	String lineText=null;
	    	while((lineText = pyPluginread.readLine())!=null){
	    		//此处备注，被以为我傻不会用：来读字符位置分隔，我是觉得可能会有人在detail里写：怕影响程序
	    		if(lineText.contains("title:")){
	    			title = lineText.substring(lineText.indexOf("title:")+6, lineText.length());
	    		}else if(lineText.contains("type:")){
	    			type = lineText.substring(lineText.indexOf("type:")+5, lineText.length());
	    		}else if(lineText.contains("autor:")){
	    			autor = lineText.substring(lineText.indexOf("autor:")+6, lineText.length());
	    		}else if(lineText.contains("detail:")){
	    			detail = lineText.substring(lineText.indexOf("detail:")+7, lineText.length());
	    		}else if(lineText.contains("}")){
	    			break;
	    		}
	    			
	    	}
	    }catch(Exception e1){
	    	e1.printStackTrace();
	    }
	    File jsonfile = new File(System.getProperty("user.dir")+"\\Setting.json");
    	JsonObject object = null;
    	JsonArray Plugins = null;
    	if(jsonfile.isFile()&&jsonfile.exists()){
    		InputStreamReader readjson = new InputStreamReader(new FileInputStream(jsonfile));
        	BufferedReader jsonread = new BufferedReader(readjson);
        	String jsonText=null;
    		if ((jsonText = jsonread.readLine())!=null){
    			//爬一下原有的json数据 以免被重写
    			JsonParser parser = new JsonParser(); 
    			object =  (JsonObject) parser.parse(new FileReader(System.getProperty("user.dir")+"\\Setting.json"));
    			Plugins = object.getAsJsonArray("Plugins");
    			for (JsonElement jsonElement : Plugins) {
    				JsonObject Plugin = jsonElement.getAsJsonObject();
    			}
    		}else{
    			object = new JsonObject();
    			Plugins = new JsonArray();
    		}
    		readjson.close();
    	}else{
    		file.createNewFile();
    		object = new JsonObject();
			Plugins = new JsonArray();
    	}
		JsonObject Plugin = new JsonObject();
	    Plugin.addProperty("title", title);
	    Plugin.addProperty("type", type);
	    Plugin.addProperty("autor", autor);
	    Plugin.addProperty("detail", detail);
	    Plugin.addProperty("path", path);
	    Plugins.add(Plugin);               // 将json对象添加到数组  
	    object.add("Plugins", Plugins);   // 将数组添加到json对象
	    String jsonStr = object.toString();   // 将json对象转化成json字符串
	    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(System.getProperty("user.dir")+"\\Setting.json")));
	    pw.print(jsonStr);
	    pw.flush();
	    pw.close();
	}
	public String getPath(String title){
		JsonParser parser = new JsonParser(); 
	    JsonObject object = null;
	    String path=null;
		try {
			object = (JsonObject) parser.parse(new FileReader(System.getProperty("user.dir")+"\\Setting.json"));
		} catch (JsonIOException e) {
			// TODO 自动生成的 catch 块
			e.printStackTrace();
		} catch (JsonSyntaxException e) {
			// TODO 自动生成的 catch 块
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			// TODO 自动生成的 catch 块
			e.printStackTrace();
		}
	    JsonArray Plugins = object.getAsJsonArray("Plugins");
	    for (JsonElement jsonElement : Plugins) {
	        JsonObject Plugin = jsonElement.getAsJsonObject();
	        if(Plugin.get("title").getAsString().equalsIgnoreCase(title)){
	        	path = Plugin.get("path").getAsString();
	        }
	    }
		return path;
	}
	public boolean isJSON(){
		File jsonfile = new File(System.getProperty("user.dir")+"\\Setting.json");
		InputStreamReader readjson = null;
		try {
			readjson = new InputStreamReader(new FileInputStream(jsonfile));
		} catch (FileNotFoundException e1) {
			// TODO 自动生成的 catch 块
			e1.printStackTrace();
		}
    	BufferedReader jsonread = new BufferedReader(readjson);
    	String jsonText=null;
    	boolean isjson=true;
    	try {
    		isjson = (jsonread.readLine()!=null);
		} catch (IOException e) {
			// TODO 自动生成的 catch 块
			e.printStackTrace();
		}
    	return isjson;
	}
}
