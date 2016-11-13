/* 米斯特安全团队 Www.Hi-OurLife.Com
 * 作者：A先森_林晨
 * Mail:admin@hi-ourlife.com
 * QQ：627437686
 */
import java.math.BigInteger;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.StringTokenizer;
import java.util.regex.Pattern;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.io.*;
import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;
import java.awt.*;
import javax.swing.*;
import javax.swing.plaf.FontUIResource;
import java.util.regex.*;
import java.awt.event.ActionListener;
//导入了Jython包 可调用python
import org.python.core.*;
import javax.script.*;  
import org.python.core.PyFunction;  
import org.python.core.PyInteger;  
import org.python.core.PyObject;  
import org.python.util.PythonInterpreter; 
import javax.imageio.*;
public class CTFcrack{
	private static String v1 = "v1.2.1";//版本号
	private static Font Zt = new Font("楷体", Font.PLAIN, 15);//字体
	JTextArea Shuru = new JTextArea();
	JTextArea ShuChu = new JTextArea();
    public void CryptoWindow(){//主窗口
		JFrame jf = new JFrame("米斯特安全团队 CTF Crypto类破解工具 pro "+v1);
		JLabel jl = new JLabel("=====填写所需检测的密码====");

		JScrollPane gShuChu = new JScrollPane(ShuChu);
		JScrollPane gShuru = new JScrollPane(Shuru);
		JLabel JieG = new JLabel("======结果======");
		JLabel AD = new JLabel("米斯特安全团队网址:www.hi-ourlife.com          程序作者:米斯特_A先森");
		JMenuBar Menu = new JMenuBar();
		JMenu zifu = new JMenu(" 解码方式");
		JMenuItem caesar = new JMenuItem(" 凯撒密码>>解码");;
		JMenuItem rot13 = new JMenuItem(" Rot13>>解码");
		JMenuItem zhalan = new JMenuItem(" 栅栏密码>>解码");
		JMenuItem peig = new JMenuItem(" 培根密码>>转换");
		JMenuItem peigd = new JMenuItem(" 培根密码>>解码");
		JMenuItem zj = new JMenuItem(" 猪圈密码>>解码");
		JMenuItem base64jg = new JMenuItem(" 字符串>>Base64(gbk)");
		JMenuItem base64cg = new JMenuItem(" Base64>>字符串(gbk)");
		JMenuItem base64j = new JMenuItem(" 字符串>>Base64(utf-8)");
		JMenuItem base64c = new JMenuItem(" Base64>>字符串(utf-8)");
		JMenuItem morsee = new JMenuItem(" 字符串>>摩斯密码");
		JMenuItem morsed = new JMenuItem(" 摩斯密码>>字符串");
		JMenuItem UrlCoded = new JMenuItem(" Url编码>>字符串");
		JMenuItem UrlCodee = new JMenuItem(" 字符串>>Url编码");
		JMenuItem UnicoderStre = new JMenuItem(" 字符串>>Unicode");
		JMenuItem UnicoderStrd = new JMenuItem(" Unicode>>字符串");
		JMenuItem asciiZUnicode = new JMenuItem(" Ascii>>Unicode");
		JMenuItem UnicodeZascii = new JMenuItem(" Unicode>>Ascii");
		JMenu jinz = new JMenu(" 进制转换");
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
		JMenu pulg = new JMenu("其他功能");
		JMenuItem unzip = new JMenuItem("压缩包");
		JMenu chaj = new JMenu(" 插件");
		JMenuItem rsa = new JMenuItem(" RSAtools");
		JMenuItem b32e = new JMenuItem(" 字符串>>Base32");
		JMenuItem b32d = new JMenuItem(" Base32>>字符串");
		JMenuItem b16e = new JMenuItem(" 字符串>>Base16");
		JMenuItem b16d = new JMenuItem(" Base16>>字符串");
		JMenu girlgif = new JMenu(" 妹子");
		JMenuItem girlgifw = new JMenuItem(" 召唤妹子");
		Container container = jf.getContentPane();
		container.setLayout(null);
		Menu.add(zifu);
		zifu.add(caesar);
		zifu.add(rot13);
		zifu.add(zhalan);
		zifu.add(peig);
		zifu.add(peigd);
		zifu.add(zj);
		zifu.add(base64j);
		zifu.add(base64c);
		zifu.add(base64jg);
		zifu.add(base64cg);
		zifu.add(morsee);
		zifu.add(morsed);
		zifu.add(UrlCoded);
		zifu.add(UrlCodee);
		zifu.add(UnicoderStre);
		zifu.add(UnicoderStrd);
		zifu.add(asciiZUnicode);
		zifu.add(UnicodeZascii);
		Menu.add(jinz);
		jinz.add(j2z8);
		jinz.add(j2z10);
		jinz.add(j2z16);
		jinz.add(j8z2);
		jinz.add(j8z10);
		jinz.add(j8z16);
		jinz.add(j10z2);
		jinz.add(j10z8);
		jinz.add(j10z16);
		jinz.add(j16z2);
		jinz.add(j16z8);
		jinz.add(j16z10);
		buildPluginMenu(chaj);//传入要添加菜单的目录
		Menu.add(chaj);
		chaj.add(rsa);
		chaj.add(b32e);
		chaj.add(b32d);
		chaj.add(b16e);
		chaj.add(b16d);
		Menu.add(girlgif);
		girlgif.add(girlgifw);
		Menu.add(pulg);
		pulg.add(unzip);
		//chaj.add(xir);
		ShuChu.setText("作者注："
			+ "\n集合栅栏 凯撒 摩斯 Base64 Url编码 Unicode等多种解码方式"
			+ "\n工具支持Python插件"
			+ "\n将写好的py脚本放进Plugin目录即可"
			+ "\n打开程序后自动遍历完成"
			+ "\n每次打开程序第一次调用python会稍慢"
			+ "\n接下来就OK了"
			+ "\n联系方式:QQ627437686"
			+ "\n懂Java的朋友也请联系我，共同开发。"
			+ "\n程序已开源 github地址：https://github.com/0Linchen/CTFcryptoCrack"
			+ "\n交流群：392613610");
		//设置Swing的属性
		jf.setVisible(true);
		//jf.setResizable(false);
		jf.setSize(720, 690);//窗口
		jf.setDefaultCloseOperation(3);
		gShuru  
		.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);  
		gShuru  
		.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);  
		gShuChu
		.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);  
		gShuChu
		.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
		container.add(jl);
		container.add(gShuru);
		container.add(AD);
		container.add(JieG);
		container.add(gShuChu);
		container.add(Menu,BorderLayout.NORTH);
		//监听按钮
		jf.addComponentListener(new ComponentAdapter(){
			@Override public void componentResized(ComponentEvent e){
				Menu.setBounds(0,
						0, 
						jf.getWidth()-20,
						20);//菜单
		    jl.setBounds(3, 
		    		20, 
		    		jf.getWidth()-20, 
		    		20);//第一个标签
		    gShuru.setBounds(3, 
		    		40, 
		    		jf.getWidth()-20, 
		    		(int)(jf.getHeight()*0.40));//输入框
		    JieG.setBounds(3, 
		    		jl.getHeight()+gShuru.getHeight()+20, 
		    		jf.getWidth()-20, 
		    		20);//结果标签
		    gShuChu.setBounds(3, 
		    		JieG.getY()+20, 
		    		jf.getWidth()-20,
		    		(int)(jf.getHeight()*0.42));//输出框
		    AD.setBounds(3, 
		    		gShuChu.getHeight()+JieG.getY()+20
		    		, jf.getWidth()-20
		    		, 20);//广告
			}});
		caesar.addActionListener(new ActionListener() {//当按下凯撒密码
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(Caesar(Shuru.getText()));
		    } } );
		peig.addActionListener(new ActionListener() {//当按下培根密码
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(peigd(Shuru.getText()));
		    } } );
		zj.addActionListener(new ActionListener() {//当按下猪圈密码
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(zjd(Shuru.getText()));
		    } } );
		rot13.addActionListener(new ActionListener() {//当按下rot13密码
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(Rot13(Shuru.getText()));
		    } } );
		zhalan.addActionListener(new ActionListener() {//当按下栅栏密码
		    public void actionPerformed(ActionEvent evt) {
		    ShuChu.setText(Zhalan(Shuru.getText()));
		    } } );
		base64j.addActionListener(new ActionListener() {//当按下Base64加密时
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(Base64j(Shuru.getText()));
		    } } );
		base64jg.addActionListener(new ActionListener() {//当按下Base64解码时
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(Base64jg(Shuru.getText()));
		    } } );
		base64cg.addActionListener(new ActionListener() {//当按下Base64解码时
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(Base64cg(Shuru.getText()));
		    } } );
		base64c.addActionListener(new ActionListener() {//当按下Base64解码时
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(Base64c(Shuru.getText()));
		    } } );
		morsee.addActionListener(new ActionListener() {//当按下摩斯加密时
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(MorseE(Shuru.getText()));
			}
		});
		morsed.addActionListener(new ActionListener() {//当按下摩斯解密时
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(MorseD(Shuru.getText()));
			}
		});
		UrlCodee.addActionListener(new ActionListener(){//当按下Url编码
		public void actionPerformed(ActionEvent evt){
			try {
				ShuChu.setText(UrlEncoder(Shuru.getText()));
			} catch (UnsupportedEncodingException e) {
				// TODO 自动生成的 catch 块
					e.printStackTrace();
				}
			}
		});
		UrlCoded.addActionListener(new ActionListener(){//当按下Url编码解码
		public void actionPerformed(ActionEvent evt){
			try {
				ShuChu.setText(UrlDecoder(Shuru.getText()));
			} catch (UnsupportedEncodingException e) {
				// TODO 自动生成的 catch 块
					e.printStackTrace();
				}
			}
		});
		UnicoderStre.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(UnicodeStre(Shuru.getText()));
			}
		});
		UnicoderStrd.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(UnicodeStrd(Shuru.getText()));
			}
		});    
		j2z8.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.toOctalString(Long.parseLong(Shuru.getText(), 2)));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j2z10.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.valueOf(Shuru.getText(),2).toString());
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j2z16.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.toHexString(Long.parseLong(Shuru.getText(), 2)));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j8z2.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.toBinaryString(Long.valueOf(Shuru.getText(),8)));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j8z10.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.valueOf(Shuru.getText(),8).toString());
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j8z16.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.toHexString(Long.valueOf(Shuru.getText(),8)));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j10z2.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.toBinaryString(Long.parseLong(Shuru.getText())));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j10z8.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.toOctalString(Long.parseLong(Shuru.getText())));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j10z16.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.toHexString(Long.parseLong(Shuru.getText())));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j16z2.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.toBinaryString(Long.valueOf(Shuru.getText(),16)));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j16z8.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.toOctalString(Long.valueOf(Shuru.getText(),16)));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j16z10.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(Long.valueOf(Shuru.getText(),16).toString());
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		UnicodeZascii.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(UnicodeZascii(Shuru.getText()));
			}
		});
		asciiZUnicode.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(asciiZUnicode(Shuru.getText()));
			}
		});
		rsa.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				new CTFcrack().rsatools();
			}
		});
		b32e.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(Base32j(Shuru.getText()));
			}
		});
		b32d.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(Base32c(Shuru.getText()));
			}
		});
		b16e.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(Base16j(Shuru.getText()));
			}
		});
		b16d.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(Base16c(Shuru.getText()));
			}
		});
		peigd.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(peigd(Shuru.getText()));
			}
		});
		girlgifw.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				new CTFcrack().girl();
				
			}
		});	
		unzip.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent e) {
			new CTFcrack().unzipgui();
			
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
    private void unzipgui(){//破解压缩包窗口 未完成
    	JFrame frame = new JFrame("zip Crack!");
    	frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
    	frame.setBounds(200,200,400,250);
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
	 new CTFcrack().CryptoWindow();//创建主窗口CryptoWindow
	}
	public String Zhalan(String Shuru){//栅栏解码
		String zlstr[]= new String[1024];
		int num = 0;
		StringBuffer jg = new StringBuffer();
		 int x[] = new int[1024];
		 int sl = Shuru.length();
		 int a = 0;
		 int i=0;
		 if (sl!=1&&sl!=2){
			 for (i=2;i<sl;i++) {
				 if ((sl%i)==0){
					 x[a]=i;
					 a = a+1;
				 }
			 }
		 }else{
			 jg.append("用肉眼就能看出来\n");
		 }
		 if (a!=0){
			 jg.append("得到因数(排除1和字符串长度):\n");
			 for(int yi=0;yi<a;yi++){
				 jg.append(" "+x[yi]);
			 }
			 jg.append("\n");
			 jg.append("\n");
			 for(i=0;i<a;i++){
				 jg.append("第"+(i+1)+"栏：");
				 for(int j=0;j<(sl/x[i]);j++){
					 zlstr[num]=(Shuru.substring((0+(x[i]*j)), (x[i]+(x[i]*j))));
					 num++;
				 }
				 int slen = zlstr[0].length();
				 for(int ji = 0;ji<slen;ji++){
					 for(int s=0;s<num;s++){
						 jg.append(zlstr[s].substring(ji, ji+1));
					 }
				 }
				 num = 0;
				 jg.append("\n");
			 }
		 }else{
			 jg.append("解码失败...\n");
			 jg.append("尝试去除字符串中的空格解码\n");
			 sl = Shuru.replace(" ", "").length();
			 jg.append(sl);
			 if (sl!=1&&sl!=2){
				 for (i=2;i<sl;i++) {
					 if ((sl%i)==0){
						 x[a]=i;
						 a = a+1;
					 }
				 }
			 }else{
				 jg.append("用肉眼就能看出来\n");
			 }
			 if (a!=0){
				 jg.append("这串密文(去除空格后)是栅栏密码...\n");
				 jg.append("得到因数(排除1和字符串长度):");
				 for(int yi=0;yi<a;yi++){
					 jg.append(" "+x[yi]);
				 }
				 jg.append("\n");
				 jg.append("\n");
				 jg.append("开始解码...");
				 for(i=0;i<a;i++){
					 jg.append("第"+(i+1)+"栏：");
					 for(int j=0;j<(sl/x[i]);j++){
						 zlstr[num]=(Shuru.substring((0+(x[i]*j)), (x[i]+(x[i]*j))));
						 num++;
					 }
					 int slen = zlstr[0].length();
					 for(int ji = 0;ji<slen;ji++){
						 for(int s=0;s<num;s++){
							 jg.append(zlstr[s].substring(ji, ji+1));
						 }
					 }
					 num = 0;
					 jg.append("\n");
				 }
		 }
	   }
	 return jg.toString();
	 }
	public String Caesar(String input){//凯撒密码
	    char[] ca = input.toCharArray();
	    int len = ca.length;
	    StringBuilder jg = new StringBuilder((len + 1) * 26);
	    for (int i = 0; i < 26; i++){
	      for (int j = 0; j < len; j++) {
	        if (isUppercase(ca[j])) {
	          if (ca[j] == 'Z') {
	            ca[j] = 'A';
	          }
	          else
	          {
	            int tmp66_64 = j;
	            char[] tmp66_63 = ca; 
	            tmp66_63[tmp66_64] = ((char)(tmp66_63[tmp66_64] + '\001'));
	          }
	        } else if (isLowercase(ca[j])){
	          if (ca[j] == 'z') {
	            ca[j] = 'a';
	          }
	          else
	          {
	            int tmp106_104 = j;
	            char[] tmp106_103 = ca; 
	            tmp106_103[tmp106_104] = ((char)(tmp106_103[tmp106_104] + '\001'));
	          }
	        }
	    }
	      jg.append(ca);
	      jg.append('\n');
		    }
	    return jg.toString();
	  }
	public String peigd(String input){//培根规律
			char ca[]=input.toCharArray();
			int pglen = ca.length;
			StringBuilder jg = new StringBuilder();
			for (int i =0;i<pglen;i++){
				if(isUppercase(ca[i])){
					ca[i]='A';
				jg.append(ca[i]);
			}else if(isLowercase(ca[i])){
				ca[i]='B';
				jg.append(ca[i]);
			}else{
			}
		}
		jg.append('\n');
	    return jg.toString();
	}
	public String zjd(String input){//猪圈密码
		char ca [] = input.toCharArray();
		int zjl = ca.length;
		StringBuilder jg = new StringBuilder();
		for (int i=0;i<zjl;i++){
			switch(ca[i]){
			 case 'A':jg.append('J');
			 break;
			 case 'B':jg.append('K');
			 break;
			 case 'C':jg.append('L');
			 break;
			 case 'D':jg.append('M');
			 break;
			 case 'E':jg.append('N');
			 break;
			 case 'F':jg.append('O');
			 break;
			 case 'G':jg.append('P');
			 break;
			 case 'H':jg.append('Q');
			 break;
			 case 'I':jg.append('R');
			 break;
			 case 'J':jg.append('A');
			 break;
			 case 'K':jg.append('B');
			 break;
			 case 'L':jg.append('C');
			 break;
			 case 'M':jg.append('D');
			 break;
			 case 'N':jg.append('E');
			 break;
			 case 'O':jg.append('F');
			 break;
			 case 'P':jg.append('G');
			 break;
			 case 'Q':jg.append('H');
			 break;
			 case 'R':jg.append('I');
			 break;
			 case 'S':jg.append('W');
			 break;
			 case 'T':jg.append('X');
			 break;
			 case 'U':jg.append('Y');
			 break;
			 case 'V':jg.append('Z');
			 break;
			 case 'W':jg.append('S');
			 break;
			 case 'X':jg.append('T');
			 break;
			 case 'Y':jg.append('U');
			 break;
			 case 'Z':jg.append('V');
			 break;
			 case 'a':jg.append('j');
			 break;
			 case 'b':jg.append('k');
			 break;
			 case 'c':jg.append('l');
			 break;
			 case 'd':jg.append('m');
			 break;
			 case 'e':jg.append('n');
			 break;
			 case 'f':jg.append('o');
			 break;
			 case 'g':jg.append('p');
			 break;
			 case 'h':jg.append('q');
			 break;
			 case 'i':jg.append('r');
			 break;
			 case 'j':jg.append('a');
			 break;
			 case 'k':jg.append('b');
			 break;
			 case 'l':jg.append('c');
			 break;
			 case 'm':jg.append('d');
			 break;
			 case 'n':jg.append('e');
			 break;
			 case 'o':jg.append('f');
			 break;
			 case 'p':jg.append('g');
			 break;
			 case 'q':jg.append('h');
			 break;
			 case 'r':jg.append('i');
			 break;
			 case 's':jg.append('w');
			 break;
			 case 't':jg.append('x');
			 break;
			 case 'u':jg.append('y');
			 break;
			 case 'v':jg.append('z');
			 break;
			 case 'w':jg.append('s');
			 break;
			 case 'x':jg.append('t');
			 break;
			 case 'y':jg.append('u');
			 break;
			 case 'z':jg.append('v');
			 break;
			 default:
				 jg.append(ca[i]);
			}
		}
		jg.append('\n');
	    return jg.toString();
	    
	}
	public String Rot13(String input){
	    StringBuilder jg = new StringBuilder();
	    for (int i = 0; i < input.length(); i++) {
	        char c = input.charAt(i);
	        if       (c >= 'a' && c <= 'm') c += 13;
	        else if  (c >= 'A' && c <= 'M') c += 13;
	        else if  (c >= 'n' && c <= 'z') c -= 13;
	        else if  (c >= 'N' && c <= 'Z') c -= 13;
	        jg.append(c);
	    }
	    return jg.toString();
	    
	}
	public String Base64c(String input){//base64解密utf-8
		StringBuffer jg = new StringBuffer();
		String jiami = null;
		try{
			jiami = new String(new BASE64Decoder().decodeBuffer(input));
		}catch(IOException e){
			e.printStackTrace();
		}
		jg.append(jiami);
		return jg.toString();
		
	}
	public String Base64j(String input){//base64加密utf-8
		StringBuffer jg = new StringBuffer();
		jg.append(new BASE64Encoder().encode(input.getBytes()));
		return jg.toString();
		
	}
	public String Base64jg(String input){//base64加密gbk
		StringBuffer jg = new StringBuffer();
	    byte[] b = null;  
	    String s = null;  
	    try {  
	        b = input.getBytes("gbk");  
	    } catch (UnsupportedEncodingException e) {  
	        e.printStackTrace();  
	    }  
	    if (b != null) {  
	        s = new BASE64Encoder().encode(b);  
	    } 
	    jg.append(s);
		return jg.toString();
		
	}
	public String Base64cg(String input){//base64解密gbk
		StringBuffer jg = new StringBuffer();
		String result = null;
		byte[] b = null;
	    if (input != null) {  
	        BASE64Decoder decoder = new BASE64Decoder();  
	        try {  
	            b = decoder.decodeBuffer(input);  
	            result = new String(b, "gbk");  
	        } catch (Exception e) {  
	            e.printStackTrace();  
	        }  
	    }  
	    jg.append(result);
		return jg.toString();
		
	}
	public String Base32j(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\basecode.py");
	    PyFunction func = (PyFunction)interpreter.get("b32e",PyFunction.class);
	    PyObject rsadstr = func.__call__(new PyString(input));  
	    return (rsadstr.toString());
	}
	public String Base32c(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\basecode.py");
	    PyFunction func = (PyFunction)interpreter.get("b32d",PyFunction.class);
	    PyObject rsadstr = func.__call__(new PyString(input));  
	    return (rsadstr.toString());
	}
	public String Base16j(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\basecode.py");
	    PyFunction func = (PyFunction)interpreter.get("b16e",PyFunction.class);
	    PyObject rsadstr = func.__call__(new PyString(input));  
	    return (rsadstr.toString());
	}
	public String Base16c(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\basecode.py");
	    PyFunction func = (PyFunction)interpreter.get("b16d",PyFunction.class);
	    PyObject rsadstr = func.__call__(new PyString(input));  
	    return (rsadstr.toString());
	}
	public String peigen(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\peigen.py");
	    PyFunction func = (PyFunction)interpreter.get("run",PyFunction.class);
	    PyObject jg = func.__call__(new PyString(input));  
	    return jg.toString();
	}
	public String MorseE(String input){//摩斯加密
		int len = input.length();
		StringBuffer jg = new StringBuffer(len *3);
		input = input.toLowerCase();
		for (int i = 0; i < len; i++)
	    {
	      char c = input.charAt(i);
	      if (isChar(c)) {
	        jg.append(morseCharacters[(c - 'a')]);
	        jg.append(" ");
	      }
	      else if (isDigit(c)) {
	        jg.append(morseDigits[(c - '0')]);
	        jg.append(" ");
	      }
	
	    }
		return jg.toString();
		
	}
	public String MorseD(String input){//摩斯解码
	  initMorseTable();
	  String morse = format(input);
	  StringTokenizer st = new StringTokenizer(morse);
	  StringBuilder jg = new StringBuilder(morse.length() / 2);
	  while (st.hasMoreTokens())
	  {
	    jg.append(htMorse.get(st.nextToken()));
	  }
	  return jg.toString();
	  
	}
	public String UrlEncoder(String input) throws UnsupportedEncodingException{//Url编码
		StringBuilder jg = new StringBuilder();
		String jm;
		jm = URLEncoder.encode(input,"utf-8");
		jg.append(jm);
		return jg.toString();
		
	}
	public String UrlDecoder(String input) throws UnsupportedEncodingException{
		StringBuilder jg = new StringBuilder();
		String jm;
		jm = URLDecoder.decode(input,"utf-8");
		jg.append(jm);
		return jg.toString();
	}
	public String UnicodeStre(String input){
		StringBuilder jg = new StringBuilder();
	    for (int i = 0; i < input.length(); i++) {	 
	        // 取出每一个字符
	        char c = input.charAt(i);
	        // 转换为unicode
	        jg.append("\\u" + Integer.toHexString(c));
	    }
	    return jg.toString();
	    
	}
	public String UnicodeStrd(String input){
		StringBuilder jg = new StringBuilder();
	    String[] hex = input.split("\\\\u");
	    for (int i = 1; i < hex.length; i++) {
	        // 转换出每一个代码点
	        int data = Integer.parseInt(hex[i], 16);
	        // 追加成string
	        jg.append((char) data);
	    }
	    return jg.toString();
	    
	}
	public String asciiZUnicode(String input){
		StringBuilder jg = new StringBuilder();
	    for (int i = 0; i < input.length(); i++) {	 
	        // 取出每一个字符
	        char c = input.charAt(i);
	        // 转换为unicode
	        jg.append("&#" + (int)(c)+";");
	    }
	    return jg.toString();
	    
	}
	public String UnicodeZascii(String input){
		StringBuilder jg = new StringBuilder();
		Pattern pattern = Pattern.compile("\\&\\#(\\d+)");
		Matcher m =pattern.matcher(input);
	    while (m.find()){  
	        jg.append((char)Integer.valueOf(m.group(1)).intValue());  
	    }
	    return jg.toString();
	    
	}
	private boolean isLowercase(char c) {//判断是否小写字母
		return (c >= 'a') && (c <= 'z');
	}
	private boolean isUppercase(char c) {//判断是否为大写字母
		return (c >= 'A') && (c <= 'Z');
	}
	private  boolean isChar(char c){//判断是否为字母
		return (isLowercase(c)) || (isUppercase(c));
	}
	private boolean isDigit(char c){//判断是否为数字
		return (c >='0')&&(c <= '9');
	}
	private String format(String input){
	    char[] ca = input.toCharArray();
	    int len = ca.length;
	    StringBuilder back = new StringBuilder(len);
	    for (int i = 0; i < len; i++)
	    {
	      switch (ca[i]) {
	      case '\n':
	        ca[i] = ' ';
	      case ' ':
	      case '-':
	      case '.':
	        back.append(ca[i]);
	      }
	    }
	    return back.toString();
	  }
	private static Hashtable<String, Character> htMorse = new Hashtable();
	// ********由团队核心 z13表哥编写的自动遍历python插件********
	private void buildPluginMenu(JMenu menu) {
		File[] dir = new File(System.getProperty("user.dir") + "\\Plugin").listFiles();
		for (File file : dir) {
			String fileName = file.getName();
			if (fileName.endsWith(".py")) {
				menu.add(buildPluginMenuItem(" "+fileName));
			}
		}
	}
	public JMenuItem buildPluginMenuItem(String filename) {
		JMenuItem item = new JMenuItem(filename);
		item.setActionCommand(filename);
		item.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				String input = Shuru.getText();
				PythonInterpreter interpreter = new PythonInterpreter();
				interpreter.execfile(System.getProperty("user.dir")
						+ "\\Plugin\\" + arg0.getActionCommand().subSequence(1,arg0.getActionCommand().length()));
				PyFunction func = (PyFunction) interpreter.get("run",
						PyFunction.class);
				PyObject jg = func.__call__(new PyString(input));
				ShuChu.setText(jg.toString());
			}
		});
		return item;
	}
	//**********************************************************
	public char morseToChar(String morse)
	  {
	    return ((Character)htMorse.get(morse)).charValue();
	  }
	public static void initMorseTable()
	  {
	    if (isInited) {
	      return;
	    }
	    for (int i = 0; i < 26; i++)
	      htMorse.put(morseCharacters[i], Character.valueOf((char)(65 + i)));
	    for (int i = 0; i < 10; i++) {
	      htMorse.put(morseDigits[i], Character.valueOf((char)(48 + i)));
	    }
	    isInited = true;
	  }
	  private static boolean isInited = false;
	  private static final String[] morseCharacters = {//摩斯密码 字母
	    ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", 
	    ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", 
	    ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.." };
	  private static final String[] morseDigits = {//摩斯密码 数字
	    "-----", ".----", "..---", "...--", "....-", 
	    ".....", "-....", "--...", "---..", "----." };
}
