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
import javax.imageio.*;
public class CTFcrack{
	private static String v1 = "v2.0 Beta";//版本号
	private static Font Zt = new Font("楷体", Font.PLAIN, 15);//字体
	JTextArea Shuru = new JTextArea(15,50);
	JTextArea ShuChu = new JTextArea();
    public void CryptoWindow(){//主窗口
    	JPanel crypto = new JPanel();
    	JTabbedPane tabbedPane = new JTabbedPane();
    	SpringLayout slt = new SpringLayout();
		JFrame jf = new JFrame("米斯特安全团队 CTFCrakTools pro "+v1);
		JLabel jl = new JLabel("填写所需检测的密码：(已输入字符数统计：0)");
		JScrollPane gShuChu = new JScrollPane(ShuChu);
		JScrollPane gShuru = new JScrollPane(Shuru);
		JLabel JieG = new JLabel("结果：(字符数统计：0)");
		JLabel AD = new JLabel("米斯特安全团队网址:www.hi-ourlife.com          程序作者:米斯特_A先森");
		JMenuBar Menu = new JMenuBar();
		JMenu zifu = new JMenu(" 解码方式");
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
		JMenu jinz = new JMenu(" 进制转换");
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
		JMenu pulg = new JMenu("其他功能");
		JMenuItem unzip = new JMenuItem("压缩包");
		JMenuItem imagewindow = new JMenuItem("图片解码");
		JMenu chaj = new JMenu(" 插件");
		JMenuItem rsa = new JMenuItem(" RSAtools");
		JMenuItem rc4 = new JMenuItem(" RC4tools");
		JMenuItem b32e = new JMenuItem(" 字符串>>Base32");
		JMenuItem b32d = new JMenuItem(" Base32>>字符串");
		JMenuItem b16e = new JMenuItem(" 字符串>>Base16");
		JMenuItem b16d = new JMenuItem(" Base16>>字符串");
		JMenu girlgif = new JMenu(" 妹子");
		JMenuItem girlgifw = new JMenuItem(" 召唤妹子");
		Container container = jf.getContentPane();
		container.setLayout(slt);
		Menu.add(zifu);
		zifu.add(caesar);
		zifu.add(rot13);
		zifu.add(fence);
		zifu.add(peig);
		zifu.add(peigd);
		zifu.add(zj);
		zifu.add(base64j);
		zifu.add(base64c);
		zifu.add(base64jg);
		zifu.add(base64cg);
		zifu.add(morsee);
		zifu.add(morsed);
		zifu.add(reverse);
		zifu.add(UrlCoded);
		zifu.add(UrlCodee);
		zifu.add(UnicoderStre);
		zifu.add(UnicoderStrd);
		zifu.add(asciiZUnicode);
		zifu.add(UnicodeZascii);
		Menu.add(jinz);
		jinz.add(radix);
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
		chaj.add(rc4);
		chaj.add(b32e);
		chaj.add(b32d);
		chaj.add(b16e);
		chaj.add(b16d);
		Menu.add(girlgif);
		girlgif.add(girlgifw);
		Menu.add(pulg);
		pulg.add(unzip);
		pulg.add(imagewindow);
		//chaj.add(xir);
		ShuChu.setText("作者注："
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
		jf.setVisible(true);
		jf.setSize(1000, 800);//窗口
		jf.setDefaultCloseOperation(3);
		//弹簧管理器
		Spring st = Spring.constant(5);
		container.add(Menu);
		slt.putConstraint(SpringLayout.NORTH, Menu, 0, SpringLayout.NORTH, container);
		slt.putConstraint(SpringLayout.WEST, Menu, 0, SpringLayout.WEST, container);
		slt.putConstraint(SpringLayout.EAST, Menu, 0, SpringLayout.EAST, container);
		container.add(jl);
		slt.putConstraint(SpringLayout.NORTH, jl, st, SpringLayout.SOUTH, Menu);
		slt.putConstraint(SpringLayout.WEST, jl, st, SpringLayout.WEST, container);
		container.add(gShuru);
		slt.putConstraint(SpringLayout.NORTH, gShuru, st, SpringLayout.SOUTH, jl);
		slt.putConstraint(SpringLayout.WEST, gShuru, st, SpringLayout.WEST, container);
		slt.putConstraint(SpringLayout.EAST, gShuru, Spring.minus(st), SpringLayout.EAST, container);
		container.add(JieG);
		slt.putConstraint(SpringLayout.NORTH, JieG, st, SpringLayout.SOUTH, gShuru);
		slt.putConstraint(SpringLayout.WEST, JieG, st, SpringLayout.WEST, container);
		container.add(gShuChu);
		slt.putConstraint(SpringLayout.NORTH, gShuChu, st, SpringLayout.SOUTH, JieG);
		slt.putConstraint(SpringLayout.WEST, gShuChu, st, SpringLayout.WEST, container);
		slt.putConstraint(SpringLayout.EAST, gShuChu, Spring.minus(st), SpringLayout.EAST, container);
		container.add(AD);
		slt.putConstraint(SpringLayout.SOUTH, gShuChu, Spring.minus(st), SpringLayout.NORTH, AD);
		slt.putConstraint(SpringLayout.SOUTH, AD, Spring.minus(st), SpringLayout.SOUTH, container);
		slt.putConstraint(SpringLayout.WEST, AD, st, SpringLayout.WEST, container);
		//container.add(crypto);
		//tabbedPane.addTab("Crypto",null,crypto,"First panel");
		//container.add(tabbedPane);
		
		//监听文本框变化
		Shuru.getDocument().addDocumentListener(new DocumentListener(){
			int inputlength;
			@Override public void changedUpdate(DocumentEvent evt) {
				inputlength = Shuru.getText().replaceAll("\r|\n", "").length();
		    	jl.setText("填写所需检测的密码：(已输入字符数统计："+inputlength+")");
		    }

			@Override
			public void insertUpdate(DocumentEvent e) {
				inputlength = Shuru.getText().replaceAll("\r|\n", "").length();
		    	jl.setText("填写所需检测的密码：(已输入字符数统计："+inputlength+")");
			}

			@Override
			public void removeUpdate(DocumentEvent e) {
				inputlength = Shuru.getText().replaceAll("\r|\n", "").length();
		    	jl.setText("填写所需检测的密码：(已输入字符数统计："+inputlength+")");
			}
		});
		ShuChu.getDocument().addDocumentListener(new DocumentListener(){
			int inputlength;
			@Override public void changedUpdate(DocumentEvent evt) {
				inputlength = ShuChu.getText().replaceAll("\r|\n", "").length();
		    	JieG.setText("结果：(字符数统计："+inputlength+")");
		    }

			@Override
			public void insertUpdate(DocumentEvent e) {
				inputlength = ShuChu.getText().replaceAll("\r|\n", "").length();
				JieG.setText("结果：(字符数统计："+inputlength+")");
			}

			@Override
			public void removeUpdate(DocumentEvent e) {
				inputlength = ShuChu.getText().replaceAll("\r|\n", "").length();
				JieG.setText("结果：(字符数统计："+inputlength+")");
			}
		});
		//监听按钮
		caesar.addActionListener(new ActionListener() {//当按下凯撒密码
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(func.Caesar(Shuru.getText()));
		    } } );
		peig.addActionListener(new ActionListener() {//当按下培根密码
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(func.Baconab(Shuru.getText()));
		    } } );
		zj.addActionListener(new ActionListener() {//当按下猪圈密码
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(func.zjd(Shuru.getText()));
		    } } );
		rot13.addActionListener(new ActionListener() {//当按下rot13密码
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(func.Rot13(Shuru.getText()));
		    } } );
		fence.addActionListener(new ActionListener() {//当按下栅栏密码
		    public void actionPerformed(ActionEvent evt) {
		    ShuChu.setText(func.Fence(Shuru.getText()));
		    } } );
		base64j.addActionListener(new ActionListener() {//当按下Base64加密时
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(func.Base64j(Shuru.getText()));
		    } } );
		base64jg.addActionListener(new ActionListener() {//当按下Base64解码时
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(func.Base64jg(Shuru.getText()));
		    } } );
		base64cg.addActionListener(new ActionListener() {//当按下Base64解码时
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(func.Base64cg(Shuru.getText()));
		    } } );
		base64c.addActionListener(new ActionListener() {//当按下Base64解码时
		    public void actionPerformed(ActionEvent evt) {
		    	ShuChu.setText(func.Base64c(Shuru.getText()));
		    } } );
		morsee.addActionListener(new ActionListener() {//当按下摩斯加密时
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.MorseE(Shuru.getText()));
			}
		});
		morsed.addActionListener(new ActionListener() {//当按下摩斯解密时
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.MorseD(Shuru.getText()));
			}
		});
		reverse.addActionListener(new ActionListener() {//当按下摩斯解密时
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.reverse(Shuru.getText()));
			}
		});
		UrlCodee.addActionListener(new ActionListener(){//当按下Url编码
		public void actionPerformed(ActionEvent evt){
			try {
				ShuChu.setText(func.UrlEncoder(Shuru.getText()));
			} catch (UnsupportedEncodingException e) {
				// TODO 自动生成的 catch 块
					e.printStackTrace();
				}
			}
		});
		UrlCoded.addActionListener(new ActionListener(){//当按下Url编码解码
		public void actionPerformed(ActionEvent evt){
			try {
				ShuChu.setText(func.UrlDecoder(Shuru.getText()));
			} catch (UnsupportedEncodingException e) {
				// TODO 自动生成的 catch 块
					e.printStackTrace();
				}
			}
		});
		UnicoderStre.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.UnicodeStre(Shuru.getText()));
			}
		});
		UnicoderStrd.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.UnicodeStrd(Shuru.getText()));
			}
		});    
		j2z8.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),2).toString(8));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j2z10.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),2).toString(10));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j2z16.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),2).toString(16));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j8z2.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),8).toString(2));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j8z10.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),8).toString(10));;
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j8z16.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),8).toString(16));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j10z2.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),10).toString(2));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j10z8.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),10).toString(8));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j10z16.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),10).toString(16));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j16z2.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),16).toString(2));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j16z8.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),16).toString(8));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		j16z10.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				try{
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),16).toString(10));
				}catch(Exception e){
					e.printStackTrace();
				}
			}
		});
		UnicodeZascii.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.UnicodeZascii(Shuru.getText()));
			}
		});
		asciiZUnicode.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.asciiZUnicode(Shuru.getText()));
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
				ShuChu.setText(func.Base32j(Shuru.getText()));
			}
		});
		b32d.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.Base32c(Shuru.getText()));
			}
		});
		b16e.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.Base16j(Shuru.getText()));
			}
		});
		b16d.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.Base16c(Shuru.getText()));
			}
		});
		peigd.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent evt){
				ShuChu.setText(func.Bacon(Shuru.getText()));
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
		imagewindow.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent e) {
			new CTFcrack().imagewindow();
			
		}
	});	
		radix.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent e) {
			new CTFcrack().radix();
			
		}
	});	
    }
    private void radix(){
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
					ShuChu.setText(new java.math.BigInteger(Shuru.getText(),2).toString(10));
				}catch(Exception e){
					e.printStackTrace();
				}
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
    private void unzipgui(){//破解压缩包窗口 未完成
    	JFrame frame = new JFrame("Zip Crack!");
    	JButton crack = new JButton("Crack");
    	JButton infile = new JButton("打开文件");
    	JCheckBox iskey = new JCheckBox("是否有密文");
    	JTextArea key = new JTextArea();
    	JComboBox select = new JComboBox();
    	JLabel filename = new JLabel("已选中文件名");
    	JLabel filepath = new JLabel("文件路径");
    	JLabel selectpydetail = new JLabel("插件详情");
    	select.addItem("选择插件");
    	filepath.setBounds(80, 40, 3000, 20);
    	filename.setBounds(235, 20, 150, 20);
    	infile.setBounds(80, 20, 150, 20);
    	select.setBounds(80, 60, 150, 20);
    	selectpydetail.setBounds(80,80,150,20);
    	iskey.setBounds(80, 100, 150, 20);
    	key.setBounds(80, 125, 150, 20);
    	key.setEditable(false);
    	crack.setBounds(80, 150, 150, 20);
    	Container container = frame.getContentPane();
    	container.add(filename);
    	container.add(filepath);
    	container.add(crack);
    	container.add(select);
    	container.add(key);
    	container.add(iskey);
    	container.add(selectpydetail);
    	container.add(infile);
    	container.setLayout(null);
    	frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
    	frame.setBounds(180,200,350,260);
    	frame.setVisible(true); 
    	String zip[] = {"zip","rar"};
    	FileNameExtensionFilter filter;
    	filter = new FileNameExtensionFilter("压缩包(.zip;.rar)",zip);
    	infile.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
    	    	JFileChooser openfile = new JFileChooser();
    	    	openfile.setFileFilter(filter);
    	    	openfile.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
    	        int openframe = openfile.showDialog(new JLabel(), "选择"); 
    	        if (openframe == JFileChooser.APPROVE_OPTION){
                File file = openfile.getSelectedFile();//得到选择的文件名
                filepath.setText(file.toString());
                filename.setText(openfile.getSelectedFile().getName());
    	    }
    		}
    	});
    	iskey.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
    			key.setEditable(iskey.isSelected());
    		}
    	});
    }
    private void imagewindow(){//破解图片窗口 未完成
    	JFrame frame = new JFrame("Image Crack!");
    	JButton crack = new JButton("Crack");
    	JButton infile = new JButton("打开文件");
    	JCheckBox iskey = new JCheckBox("是否有密文");
    	JTextArea key = new JTextArea();
    	JComboBox select = new JComboBox();
    	JLabel filename = new JLabel("已选中文件名");
    	JLabel filepath = new JLabel("文件路径");
    	JLabel selectpydetail = new JLabel("插件详情");
    	select.addItem("选择插件");
    	filepath.setBounds(80, 40, 3000, 20);
    	filename.setBounds(235, 20, 150, 20);
    	infile.setBounds(80, 20, 150, 20);
    	select.setBounds(80, 60, 150, 20);
    	selectpydetail.setBounds(80,80,150,20);
    	iskey.setBounds(80, 100, 150, 20);
    	key.setBounds(80, 125, 150, 20);
    	key.setEditable(false);
    	crack.setBounds(80, 150, 150, 20);
    	Container container = frame.getContentPane();
    	container.add(filename);
    	container.add(filepath);
    	container.add(crack);
    	container.add(select);
    	container.add(key);
    	container.add(iskey);
    	container.add(selectpydetail);
    	container.add(infile);
    	container.setLayout(null);
    	frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
    	frame.setBounds(180,200,350,260);
    	frame.setVisible(true); 
    	String image[] = {"jpg","png","bmp","pdm"};
    	String txt[] = {"txt"};
    	FileNameExtensionFilter filter,filter2;
    	JFileChooser openfile = new JFileChooser();
    	openfile.setFileSelectionMode(JFileChooser.FILES_ONLY);
    	filter = new FileNameExtensionFilter("图片(.jpg;.png;.bmp;.pdm)",image);
    	openfile.setFileFilter(filter);
    	filter2 = new FileNameExtensionFilter("文本(.txt)",txt);
    	openfile.setFileFilter(filter2);
    	infile.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
    	        int openframe = openfile.showDialog(new JLabel(), "选择"); 
    	        if (openframe == JFileChooser.APPROVE_OPTION){
                File file = openfile.getSelectedFile();//得到选择的文件名
                filepath.setText(file.toString());
                filename.setText(openfile.getSelectedFile().getName());
    	    }
    		}
    	});
    	iskey.addActionListener(new ActionListener(){
    		public void actionPerformed(ActionEvent e){
    			key.setEditable(iskey.isSelected());
    		}
    	});
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
	// ********由团队核心 z13表哥编写的自动遍历python插件********
	  private void buildPluginMenu(JMenu menu) {
		    File[] dir = new File(System.getProperty("user.dir") + "\\Plugin").listFiles();
		    for (File file : dir) {
		      String fileName = file.getName();
		      if (fileName.endsWith(".py"))
		        menu.add(buildPluginMenuItem(" " + fileName));
		    }
		  }
	public JMenuItem buildPluginMenuItem(String filename) {
	    JMenuItem item = new JMenuItem(filename);
	    item.setActionCommand(filename);
	    item.addActionListener(new ActionListener()
	    {
	      public void actionPerformed(ActionEvent arg0) {
	        String input = CTFcrack.this.Shuru.getText();
	        PythonInterpreter interpreter = new PythonInterpreter();
	        interpreter.execfile(System.getProperty("user.dir") + 
	          "\\Plugin\\" + arg0.getActionCommand().subSequence(1, arg0.getActionCommand().length()));
	        PyFunction func = (PyFunction)interpreter.get("run", 
	          PyFunction.class);
	        PyObject jg = func.__call__(new PyString(input));
	        CTFcrack.this.ShuChu.setText(jg.toString());
	      }
	    });
	    return item;
	  }
	//**********************************************************
}