package org.mstsec.CTFCrackTools;

import java.awt.EventQueue;
import java.awt.Font;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;

import org.jb2011.lnf.beautyeye.BeautyEyeLNFHelper;
import org.python.util.PythonInterpreter;
import org.python.core.*;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.awt.GridLayout;
import javax.swing.JTabbedPane;
import java.awt.event.ContainerAdapter;
import java.awt.event.ContainerEvent;
import javax.swing.JButton;
import javax.swing.JFileChooser;

import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import javax.swing.JTextArea;
import javax.swing.JPopupMenu;
import java.awt.Component;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.Properties;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.SwingConstants;
import javax.swing.JMenu;
import java.awt.Insets;
import javax.swing.JList;
import javax.swing.JLabel;
import javax.swing.*;
import javax.swing.event.ChangeListener;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.event.ChangeEvent;
import javax.swing.event.CaretListener;
import javax.swing.event.CaretEvent;
import java.awt.Color;
import javax.swing.border.LineBorder;

public class Core extends JFrame {
	private JPanel contentPane;
	private static JTextArea textArea = new JTextArea();
	private Json json =new Json();
	private static String JsonPath = new String(System.getProperty("user.dir")+"\\Setting.json");//程序配置文件
	private static String Version = "-v3.1.3";
	private static String Note = " Our team is two years old！";
	private JTextField hex2;
	private JTextField hex8;
	private JTextField hex10;
	private JTextField hex16;
	private JTextField hex32;
	private JTextField hex36;
	private JTextField inputnum;
	/**
	 * Launch the application.
	 */
	static{
		  try{
			BeautyEyeLNFHelper.frameBorderStyle=BeautyEyeLNFHelper.FrameBorderStyle.translucencySmallShadow;
		    org.jb2011.lnf.beautyeye.BeautyEyeLNFHelper.launchBeautyEyeLNF();
		    BeautyEyeLNFHelper.translucencyAtFrameInactive = true;
		    UIManager.put("RootPane.setupButtonVisible", false);
		}catch(Exception e){
			
		}
	}
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Core frame = new Core();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	/**
	 * Create the frame.
	 */
	public Core() {
		setTitle("MSTTEAM-CTFCrackTools"+Version+Note);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 906, 755);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(new GridLayout(1, 0, 0, 0));
		
		JPanel panel = new JPanel();
		panel.addContainerListener(new ContainerAdapter() {
			@Override
			public void componentRemoved(ContainerEvent arg0) {
			}
		});
		contentPane.add(panel);
		GridBagLayout gbl_panel = new GridBagLayout();
		gbl_panel.columnWidths = new int[]{0, 0};
		gbl_panel.rowHeights = new int[]{0, 0};
		gbl_panel.columnWeights = new double[]{1.0, Double.MIN_VALUE};
		gbl_panel.rowWeights = new double[]{1.0, Double.MIN_VALUE};
		panel.setLayout(gbl_panel);
		
		JTabbedPane tabbedPane = new JTabbedPane(JTabbedPane.TOP);
		GridBagConstraints gbc_tabbedPane = new GridBagConstraints();
		gbc_tabbedPane.fill = GridBagConstraints.BOTH;
		gbc_tabbedPane.gridx = 0;
		gbc_tabbedPane.gridy = 0;
		panel.add(tabbedPane, gbc_tabbedPane);
		
		JTabbedPane Crypto = new JTabbedPane(JTabbedPane.TOP);
		Crypto.addChangeListener(new ChangeListener() {
			public void stateChanged(ChangeEvent arg0) {
				textArea=(JTextArea)((JScrollPane)Crypto.getSelectedComponent()).getViewport().getView();
			}
		});
		tabbedPane.addTab("Crypto", null, Crypto, null);
		
		JScrollPane scroll0 = new JScrollPane();
		
		JTextArea Item0 = new JTextArea();
		scroll0.setViewportView(Item0);
		
		Item0.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		Item0.setText("Author:0chen\r\nTeam:MstTeam\r\n" +
				"Website:http://www.Hi-OurLife.com/\r\n" +
				"Github:https://github.com/0Chencc/CTFCrackTools\r\n" +
				"\r\n\r\nOur team is two years old！！！" +
				"\r\nHappy two years！！！");
		Crypto.addTab("0", null, scroll0, null);

		JScrollPane scroll1 = new JScrollPane();
		Crypto.addTab("1", null, scroll1, null);
		
		JTextArea Item1 = new JTextArea();
		Item1.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scroll1.setViewportView(Item1);
		
		JScrollPane scroll2 = new JScrollPane();
		Crypto.addTab("2", null, scroll2, null);
		
		JTextArea Item2 = new JTextArea();
		Item2.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scroll2.setViewportView(Item2);
		
		JScrollPane scroll3 = new JScrollPane();
		Crypto.addTab("3", null, scroll3, null);
		
		JTextArea Item3 = new JTextArea();
		Item3.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scroll3.setViewportView(Item3);
		
		JScrollPane scroll4 = new JScrollPane();
		Crypto.addTab("4", null, scroll4, null);
		JTextArea Item4 = new JTextArea();
		Item4.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scroll4.setViewportView(Item4);
		
		JScrollPane scroll5 = new JScrollPane();
		Crypto.addTab("5", null, scroll5, null);
		
		JTextArea Item5 = new JTextArea();
		Item5.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scroll5.setViewportView(Item5);
		
		JScrollPane scroll6 = new JScrollPane();
		Crypto.addTab("6", null, scroll6, null);
		
		JTextArea Item6 = new JTextArea();
		Item6.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scroll6.setViewportView(Item6);
		
		JScrollPane scroll7 = new JScrollPane();
		Crypto.addTab("7", null, scroll7, null);
		
		JTextArea Item7 = new JTextArea();
		Item7.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scroll7.setViewportView(Item7);
		
		JScrollPane scroll8 = new JScrollPane();
		Crypto.addTab("8", null, scroll8, null);
		
		JTextArea Item8 = new JTextArea();
		Item8.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scroll8.setViewportView(Item8);
		
		JScrollPane scroll9 = new JScrollPane();
		Crypto.addTab("9", null, scroll9, null);
		
		JTextArea Item9 = new JTextArea();
		Item9.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scroll9.setViewportView(Item9);
		JPopupMenu menu = new JPopupMenu();
		addPopup(Item0, menu);
		addPopup(Item1, menu);
		addPopup(Item2, menu);
		addPopup(Item3, menu);
		addPopup(Item4, menu);
		addPopup(Item5, menu);
		addPopup(Item6, menu);
		addPopup(Item7, menu);
		addPopup(Item8, menu);
		addPopup(Item9, menu);
		JMenu Decrypt = new JMenu("Decrypt");
		menu.add(Decrypt);
		
		JMenuItem CaesarCode = new JMenuItem("CaesarCode");
		CaesarCode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Caesar(textArea.getText()));
			}
		});
		Decrypt.add(CaesarCode);
		
		JMenuItem Rot13 = new JMenuItem("Rot13");
		Rot13.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Rot13(textArea.getText()));
			}
		});
		Decrypt.add(Rot13);
		
		JMenuItem Fencecode = new JMenuItem("FenceCode");
		Fencecode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Fence(textArea.getText()));
			}
		});
		Decrypt.add(Fencecode);
		
		JMenuItem Baconcode = new JMenuItem("BaconCode");
		Baconcode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Bacon(textArea.getText()));
			}
		});
		Decrypt.add(Baconcode);
		
		JMenuItem Pigcode = new JMenuItem("PigCode");
		Pigcode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.zjd(textArea.getText()));
			}
		});
		Decrypt.add(Pigcode);
		
		JMenuItem Reverse = new JMenuItem("Reverse");
		Reverse.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.reverse(textArea.getText()));
			}
		});
		Decrypt.add(Reverse);
		
		JMenuItem Ascii2Hex = new JMenuItem("Ascii->Hex");
		Ascii2Hex.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.ascii216(textArea.getText()));
			}
		});
		Decrypt.add(Ascii2Hex);
		
		JMenuItem Hex2Ascii = new JMenuItem("Hex->Ascii");
		Hex2Ascii.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				textArea.setText(Func.r162ascii(textArea.getText()));
			}
		});
		Decrypt.add(Hex2Ascii);
		
		JMenuItem Ascii2Unicode = new JMenuItem("Ascii->Unicode");
		Ascii2Unicode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.asciiZUnicode(textArea.getText()));
			}
		});
		Decrypt.add(Ascii2Unicode);
		
		JMenuItem Unicode2Ascii = new JMenuItem("Unicode->Ascii");
		Unicode2Ascii.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.UnicodeZascii(textArea.getText()));
			}
		});
		Decrypt.add(Unicode2Ascii);
		
		JMenu Decode = new JMenu("Decode");
		menu.add(Decode);
		
		JMenuItem Base64DecodeGBK = new JMenuItem("Base64DecodeGBK");
		Base64DecodeGBK.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Base64cg(textArea.getText()));
			}
		});
		Decode.add(Base64DecodeGBK);
		
		JMenuItem Base64DecodeUTF8 = new JMenuItem("Base64DecodeUTF8");
		Base64DecodeUTF8.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Base64c(textArea.getText()));
			}
		});
		Decode.add(Base64DecodeUTF8);
		
		JMenuItem Base32Decode = new JMenuItem("Base32Decode");
		Base32Decode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Base32c(textArea.getText()));
			}
		});
		Decode.add(Base32Decode);
		
		JMenuItem Base16Decode = new JMenuItem("Base16Decode");
		Base16Decode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Base16c(textArea.getText()));
			}
		});
		Decode.add(Base16Decode);
		
		JMenuItem MorseDecode = new JMenuItem("MorseDeCode");
		MorseDecode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.MorseD(textArea.getText()));
			}
		});
		Decode.add(MorseDecode);
		
		JMenuItem UrlDecode = new JMenuItem("UrlDecode");
		UrlDecode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					textArea.setText(Func.UrlDecoder(textArea.getText()));
				} catch (UnsupportedEncodingException e1) {
					// TODO 自动生成的 catch 块
					e1.printStackTrace();
				}
			}
		});
		Decode.add(UrlDecode);
		
		JMenuItem UniDecode = new JMenuItem("UnicodeDecode");
		UniDecode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.UnicodeStrd(textArea.getText()));
			}
		});
		Decode.add(UniDecode);
		
		JMenu Encode = new JMenu("Encode");
		menu.add(Encode);
		
		JMenuItem Base64Encodegbk = new JMenuItem("Base64EncodeGBK");
		Base64Encodegbk.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Base64jg(textArea.getText()));
			}
		});
		Encode.add(Base64Encodegbk);
		
		JMenuItem Base32Encode = new JMenuItem("Base32Encode");
		Base32Encode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Base32j(textArea.getText()));
			}
		});
		
		JMenuItem Base64EncodeUTF8 = new JMenuItem("Base64EncodeUTF8");
		Base64EncodeUTF8.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Base64j(textArea.getText()));
			}
		});
		Encode.add(Base64EncodeUTF8);
		Encode.add(Base32Encode);
		
		JMenuItem Base16Encode = new JMenuItem("Base16Encode");
		Base16Encode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.Base16j(textArea.getText()));
			}
		});
		Encode.add(Base16Encode);
		
		JMenuItem MorseEncode = new JMenuItem("MorseEnCode");
		MorseEncode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.MorseE(textArea.getText()));
			}
		});
		Encode.add(MorseEncode);
		
		JMenuItem UrlEncode = new JMenuItem("UrlEncode");
		UrlEncode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					textArea.setText(Func.UrlEncoder(textArea.getText()));
				} catch (UnsupportedEncodingException e1) {
					// TODO 自动生成的 catch 块
					e1.printStackTrace();
				}
			}
		});
		Encode.add(UrlEncode);
		
		JMenuItem UnicodeEncode = new JMenuItem("UnicodeEncode");
		UnicodeEncode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textArea.setText(Func.UnicodeStre(textArea.getText()));
			}
		});
		Encode.add(UnicodeEncode);
		
		JMenu Plugins = new JMenu("Plugins");
		menu.add(Plugins);
		
		DefaultListModel<String> model = new DefaultListModel<>();
		JMenuItem addPlugins = new JMenuItem("AddPlugins");
		addPlugins.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				String py_suf[] = {"py"};
		    	FileNameExtensionFilter py_filter;
		    	JFileChooser py_openfile = new JFileChooser();
		    	py_openfile.setFileSelectionMode(JFileChooser.FILES_ONLY);
		    	py_filter = new FileNameExtensionFilter("Python(.py)",py_suf);
		    	py_openfile.setFileFilter(py_filter);
		        int py_openframe = py_openfile.showDialog(new JLabel(), "选择/Choose"); 
		        if (py_openframe == JFileChooser.APPROVE_OPTION){
	            File py_file = py_openfile.getSelectedFile();//得到选择的文件名
	            try {
					String title = json.createJSON(py_file.toString());
					switch (json.getType(title)){
					case "crypto":
						Plugins.add(buildPluginMenuItem(title));
						break;
					}
					model.addElement(title);
				} catch (IOException e1) {
					e1.printStackTrace();
				} catch (Exception e1) {
					// TODO 自动生成的 catch 块
					e1.printStackTrace();
				}
		       }
			}
		});
		Plugins.add(addPlugins);
		try {
			buildCryptoPlugin(Plugins);
		} catch (Exception e1) {
			// TODO 自动生成的 catch 块
			e1.printStackTrace();
		}
		
		JPanel HexConvert = new JPanel();
		tabbedPane.addTab("HexConvert", null, HexConvert, null);
		GridBagLayout gbl_HexConvert = new GridBagLayout();
		gbl_HexConvert.columnWidths = new int[]{59, 533, 0};
		gbl_HexConvert.rowHeights = new int[]{0, 0, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 0};
		gbl_HexConvert.columnWeights = new double[]{1.0, 1.0, Double.MIN_VALUE};
		gbl_HexConvert.rowWeights = new double[]{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE};
		HexConvert.setLayout(gbl_HexConvert);
		
		JComboBox comboBox = new JComboBox();
		comboBox.setModel(new DefaultComboBoxModel(new String[] {"Binary", "Octal", "Decimal", "Hexadecimal", "32Hexadecimal", "36Hexadecimal"}));
		GridBagConstraints gbc_comboBox = new GridBagConstraints();
		gbc_comboBox.insets = new Insets(0, 0, 5, 5);
		gbc_comboBox.fill = GridBagConstraints.HORIZONTAL;
		gbc_comboBox.gridx = 0;
		gbc_comboBox.gridy = 0;
		HexConvert.add(comboBox, gbc_comboBox);
		
		inputnum = new JTextField();
		GridBagConstraints gbc_inputnum = new GridBagConstraints();
		gbc_inputnum.insets = new Insets(0, 0, 5, 0);
		gbc_inputnum.fill = GridBagConstraints.HORIZONTAL;
		gbc_inputnum.gridx = 1;
		gbc_inputnum.gridy = 0;
		HexConvert.add(inputnum, gbc_inputnum);
		inputnum.setColumns(10);
		
		JLabel lblNewLabel_7 = new JLabel("HexConvert:2/8/10/16/32/36");
		GridBagConstraints gbc_lblNewLabel_7 = new GridBagConstraints();
		gbc_lblNewLabel_7.insets = new Insets(0, 0, 5, 5);
		gbc_lblNewLabel_7.gridx = 0;
		gbc_lblNewLabel_7.gridy = 1;
		HexConvert.add(lblNewLabel_7, gbc_lblNewLabel_7);
		
		JLabel lblNewLabel = new JLabel("Result");
		GridBagConstraints gbc_lblNewLabel = new GridBagConstraints();
		gbc_lblNewLabel.insets = new Insets(0, 0, 5, 0);
		gbc_lblNewLabel.gridx = 1;
		gbc_lblNewLabel.gridy = 1;
		HexConvert.add(lblNewLabel, gbc_lblNewLabel);
		
		JLabel lblNewLabel_1 = new JLabel("Binary");
		GridBagConstraints gbc_lblNewLabel_1 = new GridBagConstraints();
		gbc_lblNewLabel_1.gridheight = 2;
		gbc_lblNewLabel_1.anchor = GridBagConstraints.ABOVE_BASELINE;
		gbc_lblNewLabel_1.insets = new Insets(0, 0, 5, 5);
		gbc_lblNewLabel_1.gridx = 0;
		gbc_lblNewLabel_1.gridy = 2;
		HexConvert.add(lblNewLabel_1, gbc_lblNewLabel_1);
		
		hex2 = new JTextField();
		hex8 = new JTextField();
		hex10 = new JTextField();
		hex16 = new JTextField();
		hex32 = new JTextField();
		hex36 = new JTextField();
		
		inputnum.addCaretListener(new CaretListener() {
			public void caretUpdate(CaretEvent e) {
				if(!inputnum.getText().equals("")){
					String input = inputnum.getText();
					input=input.replace(" ", "");
					int radixnum = 10;
					switch(comboBox.getSelectedItem().toString()){
					case "Binary":
						radixnum = 2;
						break;
					case "Octal":
						radixnum = 8;
						break;
					case "Decimal":
						radixnum = 10;
						break;
					case "Hexadecimal":
						radixnum = 16;
						break;
					case "32Hexadecimal":
						radixnum = 32;
						break;
					case "36Hexadecimal":
						radixnum = 36;
						break;
					}
					hex2.setText(new java.math.BigInteger(input,radixnum).toString(2));
					hex8.setText(new java.math.BigInteger(input,radixnum).toString(8));
					hex10.setText(new java.math.BigInteger(input,radixnum).toString(10));
					hex16.setText(new java.math.BigInteger(input,radixnum).toString(16));
					hex32.setText(new java.math.BigInteger(input,radixnum).toString(32));
					hex36.setText(new java.math.BigInteger(input,radixnum).toString(36));
				}
			}
		});
		GridBagConstraints gbc_hex2 = new GridBagConstraints();
		gbc_hex2.gridheight = 2;
		gbc_hex2.fill = GridBagConstraints.HORIZONTAL;
		gbc_hex2.insets = new Insets(0, 0, 5, 0);
		gbc_hex2.gridx = 1;
		gbc_hex2.gridy = 2;
		HexConvert.add(hex2, gbc_hex2);
		hex2.setColumns(10);
		
		JLabel lblNewLabel_2 = new JLabel("Octal");
		GridBagConstraints gbc_lblNewLabel_2 = new GridBagConstraints();
		gbc_lblNewLabel_2.gridheight = 2;
		gbc_lblNewLabel_2.insets = new Insets(0, 0, 5, 5);
		gbc_lblNewLabel_2.gridx = 0;
		gbc_lblNewLabel_2.gridy = 4;
		HexConvert.add(lblNewLabel_2, gbc_lblNewLabel_2);
		GridBagConstraints gbc_hex8 = new GridBagConstraints();
		gbc_hex8.gridheight = 2;
		gbc_hex8.fill = GridBagConstraints.HORIZONTAL;
		gbc_hex8.insets = new Insets(0, 0, 5, 0);
		gbc_hex8.gridx = 1;
		gbc_hex8.gridy = 4;
		HexConvert.add(hex8, gbc_hex8);
		hex8.setColumns(10);
		
		JLabel lblNewLabel_3 = new JLabel("Decimal");
		GridBagConstraints gbc_lblNewLabel_3 = new GridBagConstraints();
		gbc_lblNewLabel_3.gridheight = 2;
		gbc_lblNewLabel_3.insets = new Insets(0, 0, 5, 5);
		gbc_lblNewLabel_3.gridx = 0;
		gbc_lblNewLabel_3.gridy = 6;
		HexConvert.add(lblNewLabel_3, gbc_lblNewLabel_3);
		GridBagConstraints gbc_hex10 = new GridBagConstraints();
		gbc_hex10.gridheight = 2;
		gbc_hex10.fill = GridBagConstraints.HORIZONTAL;
		gbc_hex10.insets = new Insets(0, 0, 5, 0);
		gbc_hex10.gridx = 1;
		gbc_hex10.gridy = 6;
		HexConvert.add(hex10, gbc_hex10);
		hex10.setColumns(10);
		
		JLabel lblNewLabel_4 = new JLabel("Hexadecimal");
		GridBagConstraints gbc_lblNewLabel_4 = new GridBagConstraints();
		gbc_lblNewLabel_4.gridheight = 2;
		gbc_lblNewLabel_4.insets = new Insets(0, 0, 5, 5);
		gbc_lblNewLabel_4.gridx = 0;
		gbc_lblNewLabel_4.gridy = 8;
		HexConvert.add(lblNewLabel_4, gbc_lblNewLabel_4);
		
		GridBagConstraints gbc_hex16 = new GridBagConstraints();
		gbc_hex16.gridheight = 2;
		gbc_hex16.fill = GridBagConstraints.HORIZONTAL;
		gbc_hex16.insets = new Insets(0, 0, 5, 0);
		gbc_hex16.gridx = 1;
		gbc_hex16.gridy = 8;
		HexConvert.add(hex16, gbc_hex16);
		hex16.setColumns(10);
		
		JLabel lblNewLabel_5 = new JLabel("32Hexadecimal");
		GridBagConstraints gbc_lblNewLabel_5 = new GridBagConstraints();
		gbc_lblNewLabel_5.gridheight = 2;
		gbc_lblNewLabel_5.insets = new Insets(0, 0, 5, 5);
		gbc_lblNewLabel_5.gridx = 0;
		gbc_lblNewLabel_5.gridy = 10;
		HexConvert.add(lblNewLabel_5, gbc_lblNewLabel_5);
		
		GridBagConstraints gbc_hex32 = new GridBagConstraints();
		gbc_hex32.gridheight = 2;
		gbc_hex32.fill = GridBagConstraints.HORIZONTAL;
		gbc_hex32.insets = new Insets(0, 0, 5, 0);
		gbc_hex32.gridx = 1;
		gbc_hex32.gridy = 10;
		HexConvert.add(hex32, gbc_hex32);
		hex32.setColumns(10);
		
		JLabel lblNewLabel_6 = new JLabel("36Hexadecimal");
		GridBagConstraints gbc_lblNewLabel_6 = new GridBagConstraints();
		gbc_lblNewLabel_6.gridheight = 2;
		gbc_lblNewLabel_6.insets = new Insets(0, 0, 0, 5);
		gbc_lblNewLabel_6.gridx = 0;
		gbc_lblNewLabel_6.gridy = 12;
		HexConvert.add(lblNewLabel_6, gbc_lblNewLabel_6);
		
		GridBagConstraints gbc_hex36 = new GridBagConstraints();
		gbc_hex36.gridheight = 2;
		gbc_hex36.fill = GridBagConstraints.HORIZONTAL;
		gbc_hex36.gridx = 1;
		gbc_hex36.gridy = 12;
		HexConvert.add(hex36, gbc_hex36);
		hex36.setColumns(10);
		JPanel PluginsMenu = new JPanel();
		tabbedPane.addTab("PluginsMenu", null, PluginsMenu, null);
		GridBagLayout gbl_PluginsMenu = new GridBagLayout();
		gbl_PluginsMenu.columnWidths = new int[]{257, 7, 279, 0};
		gbl_PluginsMenu.rowHeights = new int[]{0, 0, 0};
		gbl_PluginsMenu.columnWeights = new double[]{1.0, 1.0, 1.0, Double.MIN_VALUE};
		gbl_PluginsMenu.rowWeights = new double[]{0.0, 1.0, Double.MIN_VALUE};
		PluginsMenu.setLayout(gbl_PluginsMenu);
		
		JLabel PluginsList = new JLabel("PluginsList");
		GridBagConstraints gbc_PluginsList = new GridBagConstraints();
		gbc_PluginsList.insets = new Insets(0, 0, 5, 5);
		gbc_PluginsList.gridx = 0;
		gbc_PluginsList.gridy = 0;
		PluginsMenu.add(PluginsList, gbc_PluginsList);
		
		JLabel PluginDetaillb = new JLabel("PluginDetail");
		GridBagConstraints gbc_PluginDetaillb = new GridBagConstraints();
		gbc_PluginDetaillb.insets = new Insets(0, 0, 5, 0);
		gbc_PluginDetaillb.gridx = 2;
		gbc_PluginDetaillb.gridy = 0;
		PluginsMenu.add(PluginDetaillb, gbc_PluginDetaillb);
		
		
		JScrollPane scrollPane = new JScrollPane();
		GridBagConstraints gbc_scrollPane = new GridBagConstraints();
		gbc_scrollPane.fill = GridBagConstraints.BOTH;
		gbc_scrollPane.gridx = 2;
		gbc_scrollPane.gridy = 1;
		PluginsMenu.add(scrollPane, gbc_scrollPane);
		
		JTextArea PluginDetail = new JTextArea();
		PluginDetail.setFont(new Font("Microsoft YaHei UI", Font.PLAIN, 13));
		scrollPane.setViewportView(PluginDetail);
		
		try {
			buildPluginMenu(model);
		} catch (Exception e1) {
			// TODO 自动生成的 catch 块
			e1.printStackTrace();
		}
		JList<String> list = new JList<>(model);
		list.setBorder(new LineBorder(Color.LIGHT_GRAY));
		list.setForeground(Color.BLACK);
		list.setBackground(Color.WHITE);
		list.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent arg0) {
				try {
					PluginDetail.setText(json.getDetail(list.getSelectedValue()));
				} catch (Exception e) {
					// TODO 自动生成的 catch 块
					e.printStackTrace();
				}
			}
		});

		GridBagConstraints gbc_list = new GridBagConstraints();
		gbc_list.insets = new Insets(0, 0, 0, 5);
		gbc_list.fill = GridBagConstraints.BOTH;
		gbc_list.gridx = 0;
		gbc_list.gridy = 1;
		PluginsMenu.add(list, gbc_list);
		
		JPanel panel_1 = new JPanel();
		GridBagConstraints gbc_panel_1 = new GridBagConstraints();
		gbc_panel_1.insets = new Insets(0, 0, 0, 5);
		gbc_panel_1.fill = GridBagConstraints.VERTICAL;
		gbc_panel_1.gridx = 1;
		gbc_panel_1.gridy = 1;
		PluginsMenu.add(panel_1, gbc_panel_1);
		GridBagLayout gbl_panel_1 = new GridBagLayout();
		gbl_panel_1.columnWidths = new int[]{69, 0};
		gbl_panel_1.rowHeights = new int[]{180, 23, 35, 23, 0};
		gbl_panel_1.columnWeights = new double[]{0.0, Double.MIN_VALUE};
		gbl_panel_1.rowWeights = new double[]{0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE};
		panel_1.setLayout(gbl_panel_1);
		//删除插件
		JButton RemovePlugin = new JButton("Remove");
		RemovePlugin.addActionListener(new ActionListener() {
			@SuppressWarnings("deprecation")
			public void actionPerformed(ActionEvent arg0) {
				try {
					String rmPlugin = list.getSelectedValue();
					switch(json.getType(rmPlugin)){
					case "crypto":
						for(int i =0;i<=Plugins.getItemCount();i++){
							if(Plugins.getItem(i).getLabel().equalsIgnoreCase(rmPlugin)){
								Plugins.remove(i);
								break;
							}
						}
						break;
					}
					model.removeElement(rmPlugin);
					json.rmPllugin(rmPlugin);
					PluginDetail.setText("");
				} catch (Exception e) {
					// TODO 自动生成的 catch 块
					e.printStackTrace();
				}
			}
		});
		//添加插件
		JButton AddPlugin = new JButton("Append");
		AddPlugin.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				String py_suf[] = {"py"};
		    	FileNameExtensionFilter py_filter;
		    	JFileChooser py_openfile = new JFileChooser();
		    	py_openfile.setFileSelectionMode(JFileChooser.FILES_ONLY);
		    	py_filter = new FileNameExtensionFilter("Python(.py)",py_suf);
		    	py_openfile.setFileFilter(py_filter);
		        int py_openframe = py_openfile.showDialog(new JLabel(), "选择/Choose"); 
		        if (py_openframe == JFileChooser.APPROVE_OPTION){
	            File py_file = py_openfile.getSelectedFile();//得到选择的文件名
	            try {
					String title = json.createJSON(py_file.toString());
					switch (json.getType(title)){
					case "crypto":
						Plugins.add(buildPluginMenuItem(title));
						break;
					}
					model.addElement(title);
				} catch (IOException e1) {
					e1.printStackTrace();
				} catch (Exception e1) {
					// TODO 自动生成的 catch 块
					e1.printStackTrace();
				}
		       }
			}
		});
		GridBagConstraints gbc_AddPlugin = new GridBagConstraints();
		gbc_AddPlugin.insets = new Insets(0, 0, 5, 0);
		gbc_AddPlugin.gridx = 0;
		gbc_AddPlugin.gridy = 1;
		panel_1.add(AddPlugin, gbc_AddPlugin);
		RemovePlugin.setHorizontalAlignment(SwingConstants.LEADING);
		GridBagConstraints gbc_RemovePlugin = new GridBagConstraints();
		gbc_RemovePlugin.gridx = 0;
		gbc_RemovePlugin.gridy = 3;
		panel_1.add(RemovePlugin, gbc_RemovePlugin);
	}
	private static void addPopup(Component component, final JPopupMenu popup) {
		component.addMouseListener(new MouseAdapter() {
		public void mousePressed(MouseEvent e) {
			if (e.isPopupTrigger()) {
				showMenu(e);
			}
		}
			public void mouseReleased(MouseEvent e) {
				if (e.isPopupTrigger()) {
					showMenu(e);
				}
			}
			private void showMenu(MouseEvent e) {
				popup.show(e.getComponent(), e.getX(), e.getY());
			}
		});
	}
	private void buildPluginMenu(DefaultListModel<String> pluginlist) throws Exception{
	    if(new File(JsonPath).isFile()&&new File(JsonPath).exists()&&json.isJSON()){
	    	FileInputStream jsonfile = new FileInputStream(JsonPath);
			InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
		    JsonParser parser = new JsonParser(); 
		    JsonObject object =  (JsonObject) parser.parse(new BufferedReader(jsonreadcoding));
	    	JsonArray Plugins = object.getAsJsonArray("Plugins");
	    	for (JsonElement jsonElement : Plugins) {
	    		JsonObject Plugin = jsonElement.getAsJsonObject();
	    		pluginlist.addElement(Plugin.get("title").getAsString());
	    	}
	    }
	}
	private void buildCryptoPlugin(JMenu menu) throws Exception{
	    if(new File(JsonPath).isFile()&&new File(JsonPath).exists()&&json.isJSON()){
	    	FileInputStream jsonfile = new FileInputStream(JsonPath);
			InputStreamReader jsonreadcoding = new InputStreamReader(jsonfile,"UTF-8");
		    JsonParser parser = new JsonParser(); 
		    JsonObject object =  (JsonObject) parser.parse(new BufferedReader(jsonreadcoding));
	    	JsonArray Plugins = object.getAsJsonArray("Plugins");
	    	for (JsonElement jsonElement : Plugins) {
	    		JsonObject Plugin = jsonElement.getAsJsonObject();
	    		if((Plugin.get("type").getAsString()).toLowerCase().equalsIgnoreCase("crypto")){
	    			menu.add(buildPluginMenuItem(Plugin.get("title").getAsString()));
	    		}
	    	}
	    }
	}
	public JMenuItem buildPluginMenuItem(String filename) throws Exception{
	    JMenuItem item = new JMenuItem(filename);
	    item.setActionCommand(filename);
	    item.addActionListener(new ActionListener(){
	      public void actionPerformed(ActionEvent arg0) {
	        String input = textArea.getText();
	        Properties props = new Properties();
	        props.put("python.home",System.getProperty("user.dir")+"/Lib");
	        props.put("python.console.encoding", "UTF-8");
	        props.put("python.security.respectJavaAccessibility", "false");
	        props.put("python.import.site","false");
	        Properties preprops = System.getProperties();
	        PythonInterpreter.initialize(preprops, props, new String[0]);
	        PythonInterpreter interpreter = new PythonInterpreter();
	        PySystemState sys = Py.getSystemState();
	        sys.path.add(System.getProperty("user.dir")+"/Lib/site-packages");
	        try {
	        	interpreter.execfile(json.getPath(arg0.getActionCommand()));
			} catch (Exception e) {
				// TODO 自动生成的 catch 块
				e.printStackTrace();
			}
	        String dialog[] = null;
	        String dialogstr = null;
	        PyFunction func =null;
	        PyObject res =null;
	        try {
				if(json.isDialog(arg0.getActionCommand())){
					dialogstr=json.getDialog(arg0.getActionCommand());
					dialog = dialogstr.split(",");
					switch (dialog.length){
					case 3:
						dialog[0]=JOptionPane.showInputDialog("Please input a "+dialog[0]);
						dialog[1]=JOptionPane.showInputDialog("Please input a "+dialog[1]);
						dialog[2]=JOptionPane.showInputDialog("Please input a "+dialog[2]);
				        func = (PyFunction)interpreter.get("main", PyFunction.class);
				        res = func.__call__(new PyString(input),new PyString(dialog[0]),new PyString(dialog[1]),new PyString(dialog[2]));
				        textArea.setText(res.toString());
				        break;
					case 2:
						dialog[0]=JOptionPane.showInputDialog("Please input a "+dialog[0]);
						dialog[1]=JOptionPane.showInputDialog("Please input a "+dialog[1]);
				        func = (PyFunction)interpreter.get("main", PyFunction.class);
				        res = func.__call__(new PyString(input),new PyString(dialog[0]),new PyString(dialog[1]));
				        textArea.setText(res.toString());
				        break;
					case 1:
						dialog[0]=JOptionPane.showInputDialog("Please input a "+dialog[0]);
						System.out.println(dialog[0]);
				        func = (PyFunction)interpreter.get("main", PyFunction.class);
				        res = func.__call__(new PyString(input),new PyString(dialog[0]));
				        textArea.setText(res.toString());
				        break;
				    default:
				    	func = (PyFunction)interpreter.get("main", PyFunction.class);
				        res = func.__call__(new PyString(input));
				        textArea.setText(res.toString());
					}
				}else{
			    	func = (PyFunction)interpreter.get("main", PyFunction.class);
			        res = func.__call__(new PyString(input));
			        textArea.setText(res.toString());
				}
			} catch (Exception e) {
				// TODO 自动生成的 catch 块
				e.printStackTrace();
			}
	      }
	    });
	    return item;
	  }
}
