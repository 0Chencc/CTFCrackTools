/* 米斯特安全团队 Www.Hi-OurLife.Com
 * 作者：A先森_林晨、Z13
 * Mail:admin@hi-ourlife.com
 * QQ：627437686
 */
import java.math.BigInteger;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.Enumeration;
import java.io.*;
import java.awt.*;
import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.plaf.FontUIResource;
//导入了Jython包 可调用python
import org.python.core.*;
import javax.script.*;  
import org.python.core.PyFunction;  
import org.python.core.PyInteger;  
import org.python.core.PyObject;  
import org.python.util.PythonInterpreter;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonIOException;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonSyntaxException;

import javax.imageio.*;
public class CTFcrack{
	private static String v1 = "v2.1 Beta";//版本号
	private static Font Zt = new Font("楷体", Font.PLAIN, 15);//字体
	public JTextArea input=new JTextArea();
	public JTextArea output=new JTextArea();
    public void CryptoWindow(){//主窗口
		//
    	CTFcrack_json json = new CTFcrack_json();//自写json接口
    	//
		JFrame jFrame = new JFrame("米斯特安全团队 CTFCrakTools pro "+v1);
		Container frameContainer= jFrame.getContentPane();
		SpringLayout springLayout = new SpringLayout();
		frameContainer.setLayout(springLayout);
		//
		JMenuBar mainMenuBar = new JMenuBar();
		JMenu Ascii = new JMenu(" 解码方式");
		JMenuItem caesar = new JMenuItem(" 凯撒密码>>解码");;
		JMenuItem rot13 = new JMenuItem(" Rot13>>解码");
		JMenuItem fence = new JMenuItem(" 栅栏密码>>解码");
		JMenuItem peig = new JMenuItem(" 培根密码>>大小写转换AB");
		JMenuItem peigd = new JMenuItem(" 培根密码>>解码");
		JMenuItem zj = new JMenuItem(" 猪圈密码>>解码");
		JMenuItem base64jg = new JMenuItem(" 字符串>>Base64(gbk)");
		JMenuItem base64cg = new JMenuItem(" Base64>>字符串(gbk)");
		JMenuItem base64j = new JMenuItem(" 字符串>>Base64(utf-8)");
		JMenuItem base64c = new JMenuItem(" Base64>>字符串(utf-8)");
		JMenuItem morsee = new JMenuItem(" 字符串>>摩斯密码");
		JMenuItem morsed = new JMenuItem(" 摩斯密码>>字符串");
		JMenuItem reverse = new JMenuItem(" 字符串>>反转");
		JMenuItem UrlCoded = new JMenuItem(" Url编码>>字符串");
		JMenuItem UrlCodee = new JMenuItem(" 字符串>>Url编码");
		JMenuItem UnicoderStre = new JMenuItem(" 字符串>>Unicode");
		JMenuItem UnicoderStrd = new JMenuItem(" Unicode>>字符串");
		JMenuItem asciiZUnicode = new JMenuItem(" Ascii>>Unicode");
		JMenuItem UnicodeZascii = new JMenuItem(" Unicode>>Ascii");
		JMenu radixchange = new JMenu(" 进制转换");
		JMenuItem radix = new JMenuItem(" 任意进制转换");
		JMenuItem j2z8 = new JMenuItem(" 二进制>>八进制");
		JMenuItem j2z10 = new JMenuItem(" 二进制>>十进制");
		JMenuItem j2z16 = new JMenuItem(" 二进制>>十六进制");
		JMenuItem j8z2 = new JMenuItem(" 八进制>>二进制");
		JMenuItem j8z10 = new JMenuItem(" 八进制>>十进制");
		JMenuItem j8z16 = new JMenuItem(" 八进制>>十六进制");
		JMenuItem j10z2 = new JMenuItem(" 十进制>>二进制");
		JMenuItem j10z8 = new JMenuItem(" 十进制>>八进制");
		JMenuItem j10z16 = new JMenuItem(" 十进制>>十六进制");
		JMenuItem j16z2 = new JMenuItem(" 十六进制>>二进制");
		JMenuItem j16z8 = new JMenuItem(" 十六进制>>八进制");
		JMenuItem j16z10 = new JMenuItem(" 十六进制>>十进制");
		JMenu Plugin = new JMenu(" 插件");
		JMenuItem addplugin = new JMenuItem(" 添加插件");
		JMenuItem rsa = new JMenuItem(" RSAtools");
		JMenuItem rc4 = new JMenuItem(" RC4tools");
		JMenuItem b32e = new JMenuItem(" 字符串>>Base32");
		JMenuItem b32d = new JMenuItem(" Base32>>字符串");
		JMenuItem b16e = new JMenuItem(" 字符串>>Base16");
		JMenuItem b16d = new JMenuItem(" Base16>>字符串");
		JMenu girlgif = new JMenu(" 妹子");
		JMenuItem girlgifw = new JMenuItem(" 召唤妹子");
		mainMenuBar.add(Ascii);
		Ascii.add(caesar);
		Ascii.add(rot13);
		Ascii.add(fence);
		Ascii.add(peig);
		Ascii.add(peigd);
		Ascii.add(zj);
		Ascii.add(base64j);
		Ascii.add(base64c);
		Ascii.add(base64jg);
		Ascii.add(base64cg);
		Ascii.add(morsee);
		Ascii.add(morsed);
		Ascii.add(reverse);
		Ascii.add(UrlCoded);
		Ascii.add(UrlCodee);
		Ascii.add(UnicoderStre);
		Ascii.add(UnicoderStrd);
		Ascii.add(asciiZUnicode);
		Ascii.add(UnicodeZascii);
		mainMenuBar.add(radixchange);
		//radixchange.add(radix);   //BUG功能....等有空修复
		radixchange.add(j2z8);
		radixchange.add(j2z10);
		radixchange.add(j2z16);
		radixchange.add(j8z2);
		radixchange.add(j8z10);
		radixchange.add(j8z16);
		radixchange.add(j10z2);
		radixchange.add(j10z8);
		radixchange.add(j10z16);
		radixchange.add(j16z2);
		radixchange.add(j16z8);
		radixchange.add(j16z10);
		buildPluginMenu(Plugin);//传入要添加菜单的目录
		mainMenuBar.add(Plugin);
		Plugin.add(addplugin);
		Plugin.add(rsa);
		Plugin.add(rc4);
		Plugin.add(b32e);
		Plugin.add(b32d);
		Plugin.add(b16e);
		Plugin.add(b16d);
		mainMenuBar.add(girlgif);
		girlgif.add(girlgifw);
		frameContainer.add(mainMenuBar);
		springLayout.putConstraint(SpringLayout.NORTH, mainMenuBar, 0, SpringLayout.NORTH, frameContainer);
		springLayout.putConstraint(SpringLayout.WEST, mainMenuBar, 0, SpringLayout.WEST, frameContainer);
		springLayout.putConstraint(SpringLayout.EAST, mainMenuBar, 0, SpringLayout.EAST, frameContainer);
		//
		JTabbedPane mainTabbedPane = new JTabbedPane();
		//
		JSplitPane crypto=new JSplitPane(JSplitPane.VERTICAL_SPLIT);
		crypto.setDividerLocation(250);
		JPanel crypto_top=new JPanel();
		crypto_top.setLayout(springLayout);
		JLabel inputL=new JLabel("填写所需检测的密码：(已输入字符数统计：0)");
		crypto_top.add(inputL);
		springLayout.putConstraint(SpringLayout.NORTH, inputL, 0, SpringLayout.NORTH, crypto_top);
		JScrollPane inputP = new JScrollPane(input);
		crypto_top.add(inputP);
		springLayout.putConstraint(SpringLayout.NORTH, inputP, 25, SpringLayout.NORTH, crypto_top);
		springLayout.putConstraint(SpringLayout.SOUTH, inputP, 0, SpringLayout.SOUTH, crypto_top);
		springLayout.putConstraint(SpringLayout.WEST, inputP, 0, SpringLayout.WEST, crypto_top);
		springLayout.putConstraint(SpringLayout.EAST, inputP, 0, SpringLayout.EAST, crypto_top);
		crypto.setTopComponent(crypto_top);
		//
		JPanel crypto_bottom=new JPanel();
		crypto_bottom.setLayout(springLayout);
		JLabel outpuL=new JLabel("结果：(字符数统计：0)");
		crypto_bottom.add(outpuL);
		springLayout.putConstraint(SpringLayout.NORTH, outpuL, 0, SpringLayout.NORTH, crypto_bottom);
		JScrollPane outputP = new JScrollPane(output);
		crypto_bottom.add(outputP);
		output.setText("作者注："
				+ "\n集合栅栏 凯撒 摩斯 Base64 Url编码 Unicode等多种解码方式"
				+ "\n备注:十六进制与字符串互相转换即为base16 在插件中可调用"
				+ "\n正在开发unzip的功能ing"
				+ "\n工具支持Python插件"
				+ "\n将写好的py脚本放进Plugin目录即可"
				+ "\n打开程序后自动遍历完成"
				+ "\n每次打开程序第一次调用python会稍慢"
				+ "\n接下来就OK了"
				+ "\n联系方式:QQ627437686"
				+ "\n懂Java的朋友也请联系我，共同开发。"
				+ "\n程序已开源 github地址：https://github.com/0Linchen/CTFCrackTools"
				+ "\n交流群：392613610");
		springLayout.putConstraint(SpringLayout.NORTH, outputP, 25, SpringLayout.NORTH, crypto_bottom);
		springLayout.putConstraint(SpringLayout.SOUTH, outputP, 0, SpringLayout.SOUTH, crypto_bottom);
		springLayout.putConstraint(SpringLayout.WEST, outputP, 0, SpringLayout.WEST, crypto_bottom);
		springLayout.putConstraint(SpringLayout.EAST, outputP, 0, SpringLayout.EAST, crypto_bottom);
		crypto.setBottomComponent(crypto_bottom);
		mainTabbedPane.addTab("Crypto", crypto);	
		//
		String image_suf[] = {"jpg","png","bmp","pdm"};
    	FileNameExtensionFilter image_filter;
    	JFileChooser image_openfile = new JFileChooser();
    	image_openfile.setFileSelectionMode(JFileChooser.FILES_ONLY);
    	image_filter = new FileNameExtensionFilter("图片(.jpg;.png;.bmp;.pdm)",image_suf);
    	image_openfile.setFileFilter(image_filter);
		JPanel image_Panel=new JPanel();
    	JButton image_crack = new JButton("Crack");
    	JButton image_infile = new JButton("打开文件");
    	JCheckBox image_iskey = new JCheckBox("是否有密文");
    	JTextArea image_key = new JTextArea();
    	image_key.setText("输入密文，如果你有打钩的话");
    	JComboBox image_select = new JComboBox();
    	JLabel image_filename = new JLabel("已选中文件名");
    	JLabel image_filepath = new JLabel("文件路径");
    	JLabel image_selectpydetail = new JLabel("插件详情");
    	JLabel image_selectlabel = new JLabel("选择插件");
    	JLabel image_iskeylabel = new JLabel("是否有密文，勾选");
    	JLabel image_setimage=new JLabel("<html>打开的图片以及破解完毕的图片会在这里显示<br/>菜鸡不会写自适应，自行调节窗口大小再打开图片</html>");
    	image_select.addItem("选择插件");
    	buildImagePluginSelectItem(image_select);
    	image_Panel.setLayout(springLayout);
		image_Panel.add(image_filename);
    	springLayout.putConstraint(SpringLayout.NORTH, image_filename, 0, SpringLayout.NORTH, image_Panel);
    	springLayout.putConstraint(SpringLayout.EAST, image_filename, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_filename, 0, SpringLayout.WEST, image_Panel);
    	image_Panel.add(image_infile);
    	springLayout.putConstraint(SpringLayout.NORTH, image_infile, 0, SpringLayout.SOUTH,image_filename);
    	springLayout.putConstraint(SpringLayout.EAST, image_infile, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_infile, 0, SpringLayout.WEST, image_Panel);
    	image_Panel.add(image_filepath);
    	springLayout.putConstraint(SpringLayout.NORTH, image_filepath, 0, SpringLayout.SOUTH,image_infile);
    	springLayout.putConstraint(SpringLayout.EAST, image_filepath, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_filepath, 0, SpringLayout.WEST, image_Panel);
    	image_key.setEditable(false);
    	image_Panel.add(image_selectlabel);
    	springLayout.putConstraint(SpringLayout.NORTH, image_selectlabel, 5, SpringLayout.SOUTH,image_filepath);
    	springLayout.putConstraint(SpringLayout.EAST, image_selectlabel, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_selectlabel, 0, SpringLayout.WEST, image_Panel);
    	image_Panel.add(image_select);
    	springLayout.putConstraint(SpringLayout.NORTH, image_select, 0, SpringLayout.SOUTH,image_selectlabel);
    	springLayout.putConstraint(SpringLayout.EAST, image_select, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_select, 0, SpringLayout.WEST, image_Panel);
    	image_Panel.add(image_iskeylabel);
    	springLayout.putConstraint(SpringLayout.NORTH, image_iskeylabel, 0, SpringLayout.SOUTH,image_select);
    	springLayout.putConstraint(SpringLayout.EAST, image_iskeylabel, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_iskeylabel, 0, SpringLayout.WEST, image_Panel);
    	image_Panel.add(image_iskey);
    	springLayout.putConstraint(SpringLayout.NORTH, image_iskey, 5, SpringLayout.SOUTH,image_iskeylabel);
    	springLayout.putConstraint(SpringLayout.EAST, image_iskey, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_iskey, 0, SpringLayout.WEST, image_Panel);
    	image_Panel.add(image_key);
    	springLayout.putConstraint(SpringLayout.NORTH, image_key, 0, SpringLayout.SOUTH,image_iskey);
    	springLayout.putConstraint(SpringLayout.EAST, image_key, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_key, 0, SpringLayout.WEST, image_Panel);
    	image_Panel.add(image_crack);
    	springLayout.putConstraint(SpringLayout.NORTH, image_crack, 0, SpringLayout.SOUTH,image_key);
    	springLayout.putConstraint(SpringLayout.EAST, image_crack, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_crack, 0, SpringLayout.WEST, image_Panel);
    	image_Panel.add(image_selectpydetail);
    	springLayout.putConstraint(SpringLayout.NORTH, image_selectpydetail, 0, SpringLayout.SOUTH,image_crack);
    	springLayout.putConstraint(SpringLayout.EAST, image_selectpydetail, 400, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_selectpydetail, 0, SpringLayout.WEST, image_Panel);
    	//
    	image_Panel.add(image_setimage);
    	springLayout.putConstraint(SpringLayout.NORTH, image_setimage, 0, SpringLayout.NORTH, image_Panel);
    	springLayout.putConstraint(SpringLayout.SOUTH, image_setimage, 0, SpringLayout.SOUTH, image_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, image_setimage, 420, SpringLayout.WEST, image_Panel);
    	springLayout.putConstraint(SpringLayout.EAST, image_setimage,-5, SpringLayout.EAST, image_Panel);
    	//
		springLayout.putConstraint(SpringLayout.NORTH, image_Panel, 0, SpringLayout.NORTH, mainTabbedPane);
		springLayout.putConstraint(SpringLayout.SOUTH, image_Panel, 0, SpringLayout.SOUTH, mainTabbedPane);
		springLayout.putConstraint(SpringLayout.EAST, image_Panel, 0, SpringLayout.EAST, mainTabbedPane);
		springLayout.putConstraint(SpringLayout.WEST, image_Panel, 0, SpringLayout.WEST, mainTabbedPane);
		mainTabbedPane.addTab("Image", image_Panel);
		//
		String zip_suf[] = {"rar","zip"};
    	FileNameExtensionFilter zip_filter;
    	JFileChooser zip_openfile = new JFileChooser();
    	zip_openfile.setFileSelectionMode(JFileChooser.FILES_ONLY);
    	zip_filter = new FileNameExtensionFilter("压缩包(.rar;.zip)",zip_suf);
    	zip_openfile.setFileFilter(zip_filter);
		JPanel zip_Panel=new JPanel();
    	JButton zip_crack = new JButton("Crack");
    	JButton zip_infile = new JButton("打开文件");
    	JCheckBox zip_iskey = new JCheckBox("是否有密文");
    	JTextArea zip_key = new JTextArea();
    	zip_key.setText("输入密文，如果你有打钩的话");
    	JComboBox zip_select = new JComboBox();
    	JLabel zip_filename = new JLabel("已选中文件名");
    	JLabel zip_filepath = new JLabel("文件路径");
    	JLabel zip_selectpydetail = new JLabel("插件详情");
    	JLabel zip_selectlabel = new JLabel("选择插件");
    	JLabel zip_iskeylabel = new JLabel("是否有密文，勾选");
    	zip_select.addItem("选择插件");
    	buildZipPluginSelectItem(zip_select);
    	zip_Panel.setLayout(springLayout);
		zip_Panel.add(zip_filename);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_filename, 0, SpringLayout.NORTH, zip_Panel);
    	springLayout.putConstraint(SpringLayout.EAST, zip_filename, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_filename, 0, SpringLayout.WEST, zip_Panel);
    	zip_Panel.add(zip_infile);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_infile, 0, SpringLayout.SOUTH,zip_filename);
    	springLayout.putConstraint(SpringLayout.EAST, zip_infile, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_infile, 0, SpringLayout.WEST, zip_Panel);
    	zip_Panel.add(zip_filepath);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_filepath, 0, SpringLayout.SOUTH,zip_infile);
    	springLayout.putConstraint(SpringLayout.EAST, zip_filepath, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_filepath, 0, SpringLayout.WEST, zip_Panel);
    	zip_key.setEditable(false);
    	zip_Panel.add(zip_selectlabel);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_selectlabel, 5, SpringLayout.SOUTH,zip_filepath);
    	springLayout.putConstraint(SpringLayout.EAST, zip_selectlabel, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_selectlabel, 0, SpringLayout.WEST, zip_Panel);
    	zip_Panel.add(zip_select);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_select, 0, SpringLayout.SOUTH,zip_selectlabel);
    	springLayout.putConstraint(SpringLayout.EAST, zip_select, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_select, 0, SpringLayout.WEST, zip_Panel);
    	zip_Panel.add(zip_iskeylabel);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_iskeylabel, 0, SpringLayout.SOUTH,zip_select);
    	springLayout.putConstraint(SpringLayout.EAST, zip_iskeylabel, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_iskeylabel, 0, SpringLayout.WEST, zip_Panel);
    	zip_Panel.add(zip_iskey);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_iskey, 5, SpringLayout.SOUTH,zip_iskeylabel);
    	springLayout.putConstraint(SpringLayout.EAST, zip_iskey, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_iskey, 0, SpringLayout.WEST, zip_Panel);
    	zip_Panel.add(zip_key);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_key, 0, SpringLayout.SOUTH,zip_iskey);
    	springLayout.putConstraint(SpringLayout.EAST, zip_key, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_key, 0, SpringLayout.WEST, zip_Panel);
    	zip_Panel.add(zip_crack);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_crack, 0, SpringLayout.SOUTH,zip_key);
    	springLayout.putConstraint(SpringLayout.EAST, zip_crack, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_crack, 0, SpringLayout.WEST, zip_Panel);
    	zip_Panel.add(zip_selectpydetail);
    	springLayout.putConstraint(SpringLayout.NORTH, zip_selectpydetail, 0, SpringLayout.SOUTH,zip_crack);
    	springLayout.putConstraint(SpringLayout.EAST, zip_selectpydetail, -300, SpringLayout.EAST, zip_Panel);
    	springLayout.putConstraint(SpringLayout.WEST, zip_selectpydetail, 0, SpringLayout.WEST, zip_Panel);
    	//
		springLayout.putConstraint(SpringLayout.NORTH, zip_Panel, 0, SpringLayout.NORTH, mainTabbedPane);
		springLayout.putConstraint(SpringLayout.SOUTH, zip_Panel, 0, SpringLayout.SOUTH, mainTabbedPane);
		springLayout.putConstraint(SpringLayout.EAST, zip_Panel, -300, SpringLayout.EAST, mainTabbedPane);
		springLayout.putConstraint(SpringLayout.WEST, zip_Panel, 0, SpringLayout.WEST, mainTabbedPane);
		mainTabbedPane.addTab("UnZip", zip_Panel);
		//
		frameContainer.add(mainTabbedPane);
		springLayout.putConstraint(SpringLayout.NORTH, mainTabbedPane, 25, SpringLayout.NORTH, frameContainer);
		springLayout.putConstraint(SpringLayout.SOUTH, mainTabbedPane, -30, SpringLayout.SOUTH, frameContainer);
		springLayout.putConstraint(SpringLayout.EAST, mainTabbedPane, 0, SpringLayout.EAST, frameContainer);
		springLayout.putConstraint(SpringLayout.WEST, mainTabbedPane, 0, SpringLayout.WEST, frameContainer);
		//
		JPanel mainBottomBar =new JPanel();
		JLabel ad=new JLabel("米斯特安全团队网址:www.hi-ourlife.com          程序作者:米斯特_A先森");
		mainBottomBar.add(ad);
		frameContainer.add(mainBottomBar);
		springLayout.putConstraint(SpringLayout.SOUTH, mainBottomBar, 0, SpringLayout.SOUTH, frameContainer);
		//
		jFrame.setDefaultCloseOperation(3);
		jFrame.setSize(1000, 800);
		jFrame.setVisible(true);
		//
    	image_infile.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
    	        int image_openframe = image_openfile.showDialog(new JLabel(), "选择"); 
    	        if (image_openframe == JFileChooser.APPROVE_OPTION){
                File image_file = image_openfile.getSelectedFile();//得到选择的文件名
                image_filepath.setText(image_file.toString());
                image_filename.setText(image_openfile.getSelectedFile().getName());
                ImageIcon newimage = new ImageIcon(image_file.toString());
                newimage.setImage(newimage.getImage().getScaledInstance(image_setimage.getWidth(),image_setimage.getHeight(), Image.SCALE_DEFAULT));
                image_setimage.setText("");
                image_setimage.setIcon(newimage);
    	    }
    		}
    	});
    	image_iskey.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
    			image_key.setEditable(image_iskey.isSelected());
    			if(image_iskey.isSelected()){
    				image_key.setText("");
    			}else{
    				image_key.setText("输入密文，如果你有打钩的话");
    			}
    		}
    	});
    	zip_infile.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
    	        int zip_openframe = zip_openfile.showDialog(new JLabel(), "选择"); 
    	        if (zip_openframe == JFileChooser.APPROVE_OPTION){
                File zip_file = zip_openfile.getSelectedFile();//得到选择的文件名
                zip_filepath.setText(zip_file.toString());
                zip_filename.setText(zip_openfile.getSelectedFile().getName());
    	    }
    		}
    	});
    	zip_iskey.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
    			zip_key.setEditable(zip_iskey.isSelected());
    			if(zip_iskey.isSelected()){
    				zip_key.setText("");
    			}else{
    				zip_key.setText("输入密文，如果你有打钩的话");
    			}
    		}
    	});
    	zip_crack.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
		        PythonInterpreter interpreter = new PythonInterpreter();
		        interpreter.execfile(json.getPath(zip_select.getSelectedItem().toString()));
		        PyFunction func = (PyFunction)interpreter.get("run", PyFunction.class);
        		if(zip_iskey.isSelected()){
        			PyObject res = func.__call__(new PyString(zip_key.getText()));
        		}else{
        			PyObject res = func.__call__();
        		}
    		}
    	});
    	image_crack.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
		        PythonInterpreter interpreter = new PythonInterpreter();
		        interpreter.execfile(json.getPath(image_select.getSelectedItem().toString()));
		        PyFunction func = (PyFunction)interpreter.get("run", PyFunction.class);
        		if(image_iskey.isSelected()){
        			PyObject res = func.__call__(new PyString(image_key.getText()));
        			image_setimage.setIcon(new ImageIcon(res.toString()));
        		}else{
        			PyObject res = func.__call__();
        			image_setimage.setIcon(new ImageIcon(res.toString()));
        		}
    		}
    	});
    	//
    	input.getDocument().addDocumentListener(new DocumentListener(){
			int inputlength;
			@Override public void changedUpdate(DocumentEvent evt) {
				inputlength = input.getText().replaceAll("\r|\n", "").length();
		    	inputL.setText("填写所需检测的密码：(已输入字符数统计："+inputlength+")");
		    }

			@Override
			public void insertUpdate(DocumentEvent e) {
				inputlength = input.getText().replaceAll("\r|\n", "").length();
		    	inputL.setText("填写所需检测的密码：(已输入字符数统计："+inputlength+")");
			}

			@Override
			public void removeUpdate(DocumentEvent e) {
				inputlength = input.getText().replaceAll("\r|\n", "").length();
		    	inputL.setText("填写所需检测的密码：(已输入字符数统计："+inputlength+")");
			}
		});
		output.getDocument().addDocumentListener(new DocumentListener(){
			int inputlength;
			@Override public void changedUpdate(DocumentEvent evt) {
				inputlength = output.getText().replaceAll("\r|\n", "").length();
		    	outpuL.setText("结果：(字符数统计："+inputlength+")");
		    }

			@Override
			public void insertUpdate(DocumentEvent e) {
				inputlength = output.getText().replaceAll("\r|\n", "").length();
				outpuL.setText("结果：(字符数统计："+inputlength+")");
			}

			@Override
			public void removeUpdate(DocumentEvent e) {
				inputlength = output.getText().replaceAll("\r|\n", "").length();
				outpuL.setText("结果：(字符数统计："+inputlength+")");
			}
		});
		//监听按钮
		caesar.addActionListener(new ActionListener() {//当按下凯撒密码
		    public void actionPerformed(ActionEvent evt) {
		    	output.setText(func.Caesar(input.getText()));
		    } } );
		peig.addActionListener(new ActionListener() {//当按下培根密码
		    public void actionPerformed(ActionEvent evt) {
		    	output.setText(func.Baconab(input.getText()));
		    } } );
		zj.addActionListener(new ActionListener() {//当按下猪圈密码
		    public void actionPerformed(ActionEvent evt) {
		    	output.setText(func.zjd(input.getText()));
		    } } );
		rot13.addActionListener(new ActionListener() {//当按下rot13密码
		    public void actionPerformed(ActionEvent evt) {
		    	output.setText(func.Rot13(input.getText()));
		    } } );
		fence.addActionListener(new ActionListener() {//当按下栅栏密码
		    public void actionPerformed(ActionEvent evt) {
		    output.setText(func.Fence(input.getText()));
		    } } );
		base64j.addActionListener(new ActionListener() {//当按下Base64加密时
		    public void actionPerformed(ActionEvent evt) {
		    	output.setText(func.Base64j(input.getText()));
		    } } );
		base64jg.addActionListener(new ActionListener() {//当按下Base64解码时
		    public void actionPerformed(ActionEvent evt) {
		    	output.setText(func.Base64jg(input.getText()));
		    } } );
		base64cg.addActionListener(new ActionListener() {//当按下Base64解码时
		    public void actionPerformed(ActionEvent evt) {
		    	output.setText(func.Base64cg(input.getText()));
		    } } );
		base64c.addActionListener(new ActionListener() {//当按下Base64解码时
		    public void actionPerformed(ActionEvent evt) {
		    	output.setText(func.Base64c(input.getText()));
		    } } );
		morsee.addActionListener(new ActionListener() {//当按下摩斯加密时
			public void actionPerformed(ActionEvent evt){
				output.setText(func.MorseE(input.getText()));
			}
		});
		morsed.addActionListener(new ActionListener() {//当按下摩斯解密时
			public void actionPerformed(ActionEvent evt){
				output.setText(func.MorseD(input.getText()));
			}
		});
		reverse.addActionListener(new ActionListener() {//当按下摩斯解密时
			public void actionPerformed(ActionEvent evt){
				output.setText(func.reverse(input.getText()));
			}
		});
		UrlCodee.addActionListener(new ActionListener(){//当按下Url编码
		public void actionPerformed(ActionEvent evt){
			try {
				output.setText(func.UrlEncoder(input.getText()));
			} catch (UnsupportedEncodingException e) {
				// 
					e.printStackTrace();
				}
			}
		});
		UrlCoded.addActionListener(new ActionListener(){//当按下Url编码解码
		public void actionPerformed(ActionEvent evt){
			try {
				output.setText(func.UrlDecoder(input.getText()));
			} catch (UnsupportedEncodingException e) {
				// 
					e.printStackTrace();
				}
			}
		});
		UnicoderStre.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				output.setText(func.UnicodeStre(input.getText()));
			}
		});
		UnicoderStrd.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				output.setText(func.UnicodeStrd(input.getText()));
			}
		});    
		j2z8.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),2).toString(8));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j2z10.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),2).toString(10));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j2z16.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),2).toString(16));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j8z2.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),8).toString(2));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j8z10.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),8).toString(10));;
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j8z16.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),8).toString(16));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j10z2.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),10).toString(2));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j10z8.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),10).toString(8));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j10z16.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),10).toString(16));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j16z2.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),16).toString(2));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j16z8.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),16).toString(8));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j16z10.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					output.setText(new java.math.BigInteger(input.getText(),16).toString(10));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		UnicodeZascii.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				output.setText(func.UnicodeZascii(input.getText()));
			}
		});
		asciiZUnicode.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				output.setText(func.asciiZUnicode(input.getText()));
			}
		});
		rsa.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				new CTFcrack().rsatools();
			}
		});
		rc4.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				new CTFcrack().rc4tools();
			}
		});
		b32e.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				output.setText(func.Base32j(input.getText()));
			}
		});
		b32d.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				output.setText(func.Base32c(input.getText()));
			}
		});
		b16e.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				output.setText(func.Base16j(input.getText()));
			}
		});
		b16d.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				output.setText(func.Base16c(input.getText()));
			}
		});
		peigd.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				output.setText(func.Bacon(input.getText()));
			}
		});
		girlgifw.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				new CTFcrack().girl();
				
			}
		});	
		radix.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent e) {
			//debug
			System.out.println(input.getText());
			new CTFcrack().radix(input.getText());
		}
	});	
		image_select.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				int index = image_select.getSelectedIndex();
				if(index != 0 ){
					try {
						image_selectpydetail.setText(json.getDetail(image_select.getSelectedItem().toString()));
					} catch (Exception e1) {
						// TODO 自动生成的 catch 块
						e1.printStackTrace();
					}
				}
			}
		});
		zip_select.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				int index = zip_select.getSelectedIndex();
				if(index != 0 ){
					try {
						zip_selectpydetail.setText(json.getDetail(zip_select.getSelectedItem().toString()));
					} catch (Exception e1) {
						// TODO 自动生成的 catch 块
						e1.printStackTrace();
					}
				}
			}
		});
		//
		String py_suf[] = {"py"};
    	FileNameExtensionFilter py_filter;
    	JFileChooser py_openfile = new JFileChooser();
    	py_openfile.setFileSelectionMode(JFileChooser.FILES_ONLY);
    	py_filter = new FileNameExtensionFilter("Python插件(.py)",py_suf);
    	py_openfile.setFileFilter(py_filter);
		addplugin.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent e) {
	        int py_openframe = py_openfile.showDialog(new JLabel(), "选择"); 
	        if (py_openframe == JFileChooser.APPROVE_OPTION){
            File py_file = py_openfile.getSelectedFile();//得到选择的文件名
            try {
				json.createJSON(py_file.toString());
				buildPluginMenu(Plugin);//传入要添加菜单的目录
			} catch (IOException e1) {
				e1.printStackTrace();
			}
	       }
		}
	});	
		//
    }
    public void radix(String input){
    	JFrame Radixgui = new JFrame("任意进制转换");
    	Radixgui.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
    	Radixgui.setLayout(null);
    	Radixgui.setBounds(0, 0, 200, 200);
    	JTextArea waitradix = new JTextArea();
    	waitradix.setBounds(10, 10, 150, 20);
    	JLabel waitTips = new JLabel("初始进制");
    	waitTips.setBounds(10,30,150,20);
    	JTextArea resradix = new JTextArea();
    	resradix.setBounds(10, 50, 150, 20);
    	JLabel resTips = new JLabel("待转换的进制");
    	resTips.setBounds(10, 70, 150, 20);
    	JButton change = new JButton("Change");
    	change.setBounds(10,90,150,20);
    	Radixgui.add(waitradix);
    	Radixgui.add(waitTips);
    	Radixgui.add(resradix);
    	Radixgui.add(resTips);
    	Radixgui.add(change);
    	Radixgui.setVisible(true);
    	Radixgui.setResizable(false);
    	change.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent evt){
				try{
		   			//int waitradixint = Integer.parseInt(waitradix.getText());
					//int resradixint = Integer.parseInt(waitradix.getText());
					//output.setText(new java.math.BigInteger(input,2).toString(10)); //debug
				}catch(Exception e){
					//debug
					e.printStackTrace();
				}
				System.out.println(output.getText());
    		}
    	});
    }
    private void rsatools(){//rsatools窗口
        JFrame Rsatools = new JFrame("RsaTools--Python插件");
        JTextArea rsap = new JTextArea();
        JTextArea rsaq = new JTextArea();
        JTextArea rsae = new JTextArea();
        JTextArea rsad = new JTextArea();
        JLabel Rlabelp = new JLabel("p:");
        JLabel Rlabelq = new JLabel("q:");
        JLabel Rlabele = new JLabel("e:");
        JLabel Rlabeld = new JLabel("d:");
        JButton rsady = new JButton("Calc.D");
        Container container = Rsatools.getContentPane();
        container.setLayout(null);
        Rsatools.setVisible(true);
        Rsatools.setResizable(false);
        Rsatools.setSize(300, 200);//窗口
        Rsatools.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        rsap.setBounds(30, 10, 200,20);
        rsaq.setBounds(30, 40,200, 20);
        rsae.setBounds(30, 70, 200, 20);
        rsad.setBounds(30, 100, 200, 20);
        container.add(rsap);
        container.add(rsaq);
        container.add(rsae);
        container.add(rsad);
        Rlabelp.setBounds(5, 10, 30, 20);
        Rlabelq.setBounds(5, 40,30,20);
        Rlabele.setBounds(5, 70, 30, 20);
        Rlabeld.setBounds(5, 100, 30, 20);
        container.add(Rlabelp);
        container.add(Rlabelq);
        container.add(Rlabele);
        container.add(Rlabeld);
        rsady.setBounds(80, 130, 100, 20);
        container.add(rsady);
    	rsady.addActionListener(new ActionListener(){//调用rsatools
    		public void actionPerformed(ActionEvent evt){
             PythonInterpreter interpreter = new PythonInterpreter();
    		 interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\rsa.py");
    		 BigInteger rsapstr=new BigInteger(rsap.getText());
             BigInteger rsaqstr=new BigInteger(rsaq.getText());
             BigInteger rsaestr=new BigInteger(rsae.getText());
             PyFunction func = (PyFunction)interpreter.get("rsa",PyFunction.class);
             PyObject rsadstr = func.__call__(new PyLong(rsapstr), new PyLong(rsaqstr),new PyLong(rsaestr));  
             rsad.setText(rsadstr.toString());
    		}
    	});
    }
    private void rc4tools(){//rsatools窗口
        JFrame Rc4tools = new JFrame("rc4--Python插件");
        JTextArea datat = new JTextArea();
        JTextArea keyt = new JTextArea();
        JTextArea rest = new JTextArea();
        JLabel Rdata = new JLabel("data");
        JLabel Rkey = new JLabel("key");
        JLabel Rres = new JLabel("Res");
        JButton RC4crack = new JButton("Crack!");
        Container container = Rc4tools.getContentPane();
        container.setLayout(null);
        Rc4tools.setVisible(true);
        Rc4tools.setResizable(false);
        Rc4tools.setSize(300, 170);//窗口
        Rc4tools.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        datat.setBounds(50, 10, 200,20);
        keyt.setBounds(50, 40,200, 20);
        rest.setBounds(50, 70, 200, 20);
        container.add(datat);
        container.add(keyt);
        container.add(rest);
        Rdata.setBounds(5, 10, 50, 20);
        Rkey.setBounds(5, 40,50,20);
        Rres.setBounds(5, 70, 50, 20);
        container.add(Rdata);
        container.add(Rkey);
        container.add(Rres);
        RC4crack.setBounds(80, 100, 100, 20);
        container.add(RC4crack);
    	RC4crack.addActionListener(new ActionListener(){//调用rsatools
    		public void actionPerformed(ActionEvent evt){
             PythonInterpreter interpreter = new PythonInterpreter();
    		 interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\RC4.py");
    		 String data=datat.getText();
             String key=keyt.getText();
             PyFunction func = (PyFunction)interpreter.get("main",PyFunction.class);
             PyObject rsadstr = func.__call__(new PyString(data), new PyString(key));  
             rest.setText(rsadstr.toString());
    		}
    	});
    }
    private void girl(){//妹子窗口
        JFrame frame = new JFrame("可爱的我来啦！"); 
        frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); 
        File imgadd = new File(System.getProperty("user.dir")+"\\girl\\girl1.gif");
        ImageIcon imageIcon = new ImageIcon(imgadd.toString()); 
        JLabel label = new JLabel("", imageIcon, SwingConstants.CENTER); 
        frame.add(label); 
        frame.pack(); 
        frame.setVisible(true); 
    }
    private static void InitGlobalFont(Font font) {//设置全局统一字体
		  FontUIResource fontRes = new FontUIResource(font);  
		  for (Enumeration<Object> keys = UIManager.getDefaults().keys();  
		  keys.hasMoreElements(); ) {  
		  Object key = keys.nextElement();  
		  Object value = UIManager.get(key);  
		  if (value instanceof FontUIResource) {  
		  UIManager.put(key, fontRes);  
		 }
	  }
	}  
	public static void main(String[] args){//主方法 
	 InitGlobalFont(Zt);//赋值字体
	 
	 String help = (  "*****************************************************"
			    +   "\n*                                                   *"
			    +   "\n*                                                   *"
			    +   "\n*             Weclome to CTFcrackTools              *"
			    +   "\n*             Autor:0chen                           *"
			    +   "\n*             Team:Mr Sec Team                      *"
			    +   "\n*             Site:www.hi-ourlife.com               *"
			    +   "\n*                                                   *"
			    +   "\n*                                                   *"
			    +   "\n*****************************************************"
			    +   "\n\nUsage:CTFcrack.jar [-options] [password]\n"
			    +   "\n-caesar  //This is Crack Caesar Code  调用凯撒密码解码"
				+   "\n-rot13   //This is Crack Rot13 Code   调用rot13解码"
				+   "\n-fence   //This is Crack Fence Code   调用栅栏密码解码"
				+   "\n-bcab    //This is Bacon Upper and    培根大小写转换AB"
				+   "\n           Lower case change to AB"
				+   "\n-bcd     //This is Crack Bacon Code   培根密码AB解码"
				+   "\n-pig     //This is Crack Pig Code     猪圈密码对调");
	 if (args.length==0){
	 }else{
	 switch(args[0]){
		case "-h":
			System.out.println(help);
			System.exit(0);
			break;
		case "-caesar":
			System.out.println(func.Caesar(args[1]));
			System.exit(0);
			break;
		case "-rot13":
			System.out.println(func.Rot13(args[1]));
			System.exit(0);
			break;
		case "-fence":
			System.out.println(func.Fence(args[1]));
			System.exit(0);
			break;
		case "-bcab":
			System.out.println(func.Baconab(args[1]));
			System.exit(0);
			break;
		case "-bcd":
			System.out.println(func.Bacon(args[1]));
			System.exit(0);
			break;
		case "-pig":
			System.out.println(func.zjd(args[1]));
			System.exit(0);
			break;
		default:
			System.out.println("\nMaybe you are make a mistake!\n\n"+help);
			System.exit(0);
			break;
	  }
	 }
	 new CTFcrack().CryptoWindow();//创建主窗口CryptoWindow
	}
	//菜单
	private void buildPluginMenu(JMenu menu) {
		//
		CTFcrack_json json = new CTFcrack_json();
	    File jsonfile = new File(System.getProperty("user.dir")+"\\Setting.json");
	    if(jsonfile.isFile()&&jsonfile.exists()&&json.isJSON()){
	    	JsonParser parser = new JsonParser(); 
	    	JsonObject object = null;
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
	    		String a=null;
	    		if(Plugin.get("type").getAsString().equalsIgnoreCase("crypto")){
	    			menu.add(buildPluginMenuItem(" " + Plugin.get("title").getAsString()));
	    		}
	    	}
	    }
	}
	private void buildZipPluginSelectItem(JComboBox Item) {
	    //
		CTFcrack_json json = new CTFcrack_json();
	    File jsonfile = new File(System.getProperty("user.dir")+"\\Setting.json");
	    if(jsonfile.isFile()&&jsonfile.exists()&&json.isJSON()){
	    	JsonParser parser = new JsonParser(); 
	    	JsonObject object = null;
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
		    		if(Plugin.get("type").getAsString().equalsIgnoreCase("zip")){
		    			Item.addItem(Plugin.get("title").getAsString());
		    	}
		    }
	    }
	  }
	private void buildImagePluginSelectItem(JComboBox Item) {
	    //
		CTFcrack_json json = new CTFcrack_json();
	    File jsonfile = new File(System.getProperty("user.dir")+"\\Setting.json");
	    if(jsonfile.isFile()&&jsonfile.exists()&&json.isJSON()){
	    	JsonParser parser = new JsonParser(); 
	    	JsonObject object = null;
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
		    		if(Plugin.get("type").getAsString().equalsIgnoreCase("image")){
		    			Item.addItem(Plugin.get("title").getAsString());
		    		}
	    	}
	    }
	  }
	public JMenuItem buildPluginMenuItem(String filename) {
		JsonParser parser = new JsonParser(); 
	    JsonObject object = null;
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
	    //
	    JMenuItem item = new JMenuItem(filename);
	    item.setActionCommand(filename);
	    item.addActionListener(new ActionListener(){
	      public void actionPerformed(ActionEvent arg0) {
	        String input = CTFcrack.this.input.getText();
	        PythonInterpreter interpreter = new PythonInterpreter();
	        for (JsonElement jsonElement : Plugins) {
		        JsonObject Plugin = jsonElement.getAsJsonObject();
		        if(Plugin.get("title").getAsString().equalsIgnoreCase(arg0.getActionCommand().substring(1, arg0.getActionCommand().length()))){
		        	interpreter.execfile(Plugin.get("path").getAsString());
		        }
		    }
	        PyFunction func = (PyFunction)interpreter.get("run", PyFunction.class);
	        PyObject res = func.__call__(new PyString(input));
	        CTFcrack.this.output.setText(res.toString());
	      }
	    });
	    return item;
	  }
		//
}