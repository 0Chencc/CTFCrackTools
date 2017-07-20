package org.mstsec.CTFcrackTools;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.*;
import com.google.gson.*;
import com.google.gson.reflect.TypeToken;
public class Json{
	String JsonPath = new String(System.getProperty("user.dir")+"\\Setting.json");
	//Json解析
	public String getType(String title) throws Exception{
		FileInputStream jsonfile = new FileInputStream(JsonPath);
		InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
	    JsonParser parser = new JsonParser(); 
	    JsonObject object =  (JsonObject) parser.parse(new BufferedReader(jsonreadcoding));
	    String type=null;
	    JsonArray Plugins = object.getAsJsonArray("Plugins");
	    for (JsonElement jsonElement : Plugins) {
	        JsonObject Plugin = jsonElement.getAsJsonObject();
	        if(Plugin.get("title").getAsString().equalsIgnoreCase(title)){
	        	type =  Plugin.get("type").getAsString();
	        }
	    }
		return type;
	}
	public String getDialog(String title) throws Exception{
		FileInputStream jsonfile = new FileInputStream(JsonPath);
		InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
	    JsonParser parser = new JsonParser(); 
	    JsonObject object =  (JsonObject) parser.parse(new BufferedReader(jsonreadcoding));
	    String Dialog=null;
	    JsonArray Plugins = object.getAsJsonArray("Plugins");
	    for (JsonElement jsonElement : Plugins) {
	        JsonObject Plugin = jsonElement.getAsJsonObject();
	        if(Plugin.get("title").getAsString().equalsIgnoreCase(title)){
	        	Dialog =  Plugin.get("dialog").getAsString();
	        }
	    }
		return Dialog;
	}
	public Boolean isDialog(String title) throws Exception{
		FileInputStream jsonfile = new FileInputStream(JsonPath);
		InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
	    JsonParser parser = new JsonParser(); 
	    JsonObject object =  (JsonObject) parser.parse(new BufferedReader(jsonreadcoding));
	    JsonArray Plugins = object.getAsJsonArray("Plugins");
	    for (JsonElement jsonElement : Plugins) {
	        JsonObject Plugin = jsonElement.getAsJsonObject();
	        if(Plugin.get("title").getAsString().equalsIgnoreCase(title)){
	        	if(!Plugin.get("dialog").isJsonNull()){
	        		return true;
	        	}
	        }
	    }
		return false;
		
	}
	public String getAuthor(String title) throws Exception{
		FileInputStream jsonfile = new FileInputStream(JsonPath);
		InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
	    JsonParser parser = new JsonParser(); 
	    JsonObject object =  (JsonObject) parser.parse(new BufferedReader(jsonreadcoding));
	    String author=null;
	    JsonArray Plugins = object.getAsJsonArray("Plugins");
	    for (JsonElement jsonElement : Plugins) {
	        JsonObject Plugin = jsonElement.getAsJsonObject();
	        if(Plugin.get("title").getAsString().equalsIgnoreCase(title)){
	        	author =  Plugin.get("author").getAsString();
	        }
	    }
		return author;
	}
	public String getDetail(String title) throws Exception{
	    // 创建json解析器
		FileInputStream jsonfile = new FileInputStream(JsonPath);
		InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
	    JsonParser parser = new JsonParser(); 
	    JsonObject object =  (JsonObject) parser.parse(new BufferedReader(jsonreadcoding));
	    String detailStr=null;
	    JsonArray Plugins = object.getAsJsonArray("Plugins");
	    for (JsonElement jsonElement : Plugins) {
	        JsonObject Plugin = jsonElement.getAsJsonObject();
	        if(Plugin.get("title").getAsString().equalsIgnoreCase(title)&&!Plugin.get("dialog").isJsonNull()){
	        	detailStr = "Title:"+Plugin.get("title").getAsString()+"\n\n"
	        				+ "Author："+Plugin.get("author").getAsString()+"\n\n"
	        				+"Type："+Plugin.get("type").getAsString()+"\n\n"
	        				+ "Detail："+Plugin.get("detail").getAsString()+"\n\n"
	        				+ "Dialog："+Plugin.get("dialog").getAsString()+"\n\n"
	        				+ "Path："+Plugin.get("path").getAsString();
	        }else if(Plugin.get("title").getAsString().equalsIgnoreCase(title)&&Plugin.get("dialog").isJsonNull()){
	        	detailStr = "Title："+Plugin.get("title").getAsString()+"\n\n"
        				+ "Author："+Plugin.get("author").getAsString()+"\n\n"
        				+"Type："+Plugin.get("type").getAsString()+"\n\n"
        				+ "Detail："+Plugin.get("detail").getAsString()+"\n\n"
        				+ "Path："+Plugin.get("path").getAsString();
	        }
	    }
	    return detailStr;
	}
	//对添加的插件进行解析，然后添加至菜单栏。并调用写入配置方法
	public String createJSON(String path) throws IOException{
		String title=null,type=null,author=null,detail=null,dialog=null;
	    try{
	    	FileInputStream pypath = new FileInputStream(path);
			InputStreamReader readpy = new InputStreamReader(pypath,"UTF-8");
	    	BufferedReader pyPluginread = new BufferedReader(readpy);
	    	String lineText=null;
	    		while((lineText = pyPluginread.readLine())!=null){
		    		if(lineText.toLowerCase().contains("title:")){
		    			title = lineText.substring(lineText.toLowerCase().indexOf("title:")+6, lineText.length());
		    		}else if(lineText.toLowerCase().contains("type:")){
		    			type = lineText.substring(lineText.toLowerCase().indexOf("type:")+5, lineText.length());
		    		}else if(lineText.toLowerCase().contains("author:")){
		    			author = lineText.substring(lineText.toLowerCase().indexOf("author:")+7, lineText.length());
		    		}else if(lineText.toLowerCase().contains("detail:")){
		    			detail = lineText.substring(lineText.toLowerCase().indexOf("detail:")+7, lineText.length());
		    		}else if(lineText.toLowerCase().contains("dialog:")){
		    			dialog = lineText.substring(lineText.toLowerCase().indexOf("dialog:")+7, lineText.length());
		    		}else if(lineText.contains("}")){
		    			break;
		    		}
	    		
	    		}
	    }catch(Exception e1){
	    	e1.printStackTrace();
	    }
	    FileInputStream jsonfile = new FileInputStream(path);
    	JsonObject object = null;
    	JsonArray Plugins = null;
    	if(new File(JsonPath).isFile()&&new File(JsonPath).exists()){
    		InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
        	BufferedReader jsonread = new BufferedReader(jsonreadcoding);
        	String jsonText=null;
    		if ((jsonText = jsonread.readLine())!=null){
    			//爬一下原有的json数据 以免被重写
    			JsonParser parser = new JsonParser(); 
    			object =  (JsonObject) parser.parse(new FileReader(JsonPath));
    			Plugins = object.getAsJsonArray("Plugins");
    			for (JsonElement jsonElement : Plugins) {
    				JsonObject Plugin = jsonElement.getAsJsonObject();
    			}
    		}else{
    			object = new JsonObject();
    			Plugins = new JsonArray();
    		}
    		jsonreadcoding.close();
    	}else{
    		new File(JsonPath).createNewFile();
    		object = new JsonObject();
			Plugins = new JsonArray();
    	}
		JsonObject Plugin = new JsonObject();
		JsonFormatTool tool = new JsonFormatTool();
	    Plugin.addProperty("title", title);
	    Plugin.addProperty("type", type);
	    Plugin.addProperty("author", author);
	    Plugin.addProperty("detail", detail);
	    Plugin.addProperty("dialog", dialog);
	    Plugin.addProperty("path", path);
	    Plugins.add(Plugin);               // 将json对象添加到数组  
	    object.add("Plugins", Plugins);   // 将数组添加到json对象
	    String jsonStr = object.toString();   // 将json对象转化成json字符串
	    FileOutputStream outfile = new FileOutputStream(JsonPath);
	    OutputStreamWriter outprint = new OutputStreamWriter(outfile,"UTF-8");
	    outprint.write(tool.formatJson(jsonStr));
	    outprint.flush();
	    return title;
	}
	public void rmPllugin(String title)throws Exception{
	    FileInputStream jsonfile = new FileInputStream(JsonPath);
    	JsonObject object = null;
    	JsonArray Plugins = null;
    	if(new File(JsonPath).isFile()&&new File(JsonPath).exists()){
    		InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
        	BufferedReader jsonread = new BufferedReader(jsonreadcoding);
        	String jsonText=null;
    		if ((jsonText = jsonread.readLine())!=null){
    			//爬一下原有的json数据 以免被重写
    			JsonParser parser = new JsonParser(); 
    			object =  (JsonObject) parser.parse(new FileReader(JsonPath));
    			Plugins = object.getAsJsonArray("Plugins");
    			for (JsonElement jsonElement : Plugins) {
    				JsonObject Plugin = jsonElement.getAsJsonObject();
    			}
    		}
    		jsonreadcoding.close();
    	}
	    //
	    for (JsonElement jsonElement : Plugins) {
	        JsonObject Plugin = jsonElement.getAsJsonObject();
	        if(Plugin.get("title").getAsString().equalsIgnoreCase(title)){
	        	Plugins.remove(Plugin);
	        	break;
	        }
	    }
		JsonFormatTool tool = new JsonFormatTool();
	    object.add("Plugins", Plugins);   // 将数组添加到json对象
	    String jsonStr = object.toString();   // 将json对象转化成json字符串
	    FileOutputStream outfile = new FileOutputStream(JsonPath);
	    OutputStreamWriter outprint = new OutputStreamWriter(outfile,"UTF-8");
	    outprint.write(tool.formatJson(jsonStr));
	    outprint.flush();
	}
	public String getPath(String title) throws Exception{
	    String path=null;
		FileInputStream jsonfile = new FileInputStream(JsonPath);
		InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
	    JsonParser parser = new JsonParser(); 
	    JsonObject object =  (JsonObject) parser.parse(new BufferedReader(jsonreadcoding));
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
		File jsonfile = new File(JsonPath);
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
