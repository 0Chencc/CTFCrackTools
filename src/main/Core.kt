import javax.swing.JFrame
import javax.swing.JPanel
import javax.swing.border.EmptyBorder
import org.python.util.PythonInterpreter
import org.python.core.*
import com.google.gson.JsonObject
import com.google.gson.JsonParser
import org.apache.commons.lang3.*
import java.awt.*
import java.awt.event.*

import javax.swing.JTabbedPane
import javax.swing.JButton
import javax.swing.JFileChooser

import javax.swing.JTextArea
import javax.swing.JPopupMenu
import java.io.BufferedReader
import java.io.File
import java.io.FileInputStream
import java.io.IOException
import java.io.InputStreamReader
import java.lang.Double
import java.math.BigInteger
import java.util.Properties
import javax.swing.JMenuItem
import javax.swing.JOptionPane
import javax.swing.SwingConstants
import javax.swing.JMenu
import javax.swing.JList
import javax.swing.JLabel
import javax.swing.*

import javax.swing.filechooser.FileNameExtensionFilter
import javax.swing.border.LineBorder
import javax.swing.text.DefaultEditorKit

import mdlaf.*
import mdlaf.animation.*
import org.jb2011.lnf.beautyeye.BeautyEyeLNFHelper
import com.alee.laf.WebLookAndFeel
import mdlaf.utils.MaterialColors

import org.python.google.common.html.HtmlEscapers

class Core : JFrame() {
    internal var f=Func()
    private val contentPane: JPanel
    private val json=Json()
    private val hex2: JTextField
    private val hex8: JTextField
    private val hex10: JTextField
    private val hex16: JTextField
    private val hex32: JTextField
    private val hex36: JTextField
    private val inputnum: JTextField

    /**
     * Create the frame.
     */
    init {
        val imJArea: InputMap=UIManager.get("TextArea.focusInputMap") as InputMap
        val imJField: InputMap=UIManager.get("TextField.focusInputMap") as InputMap
        val os=System.getProperty("os.name")
        if(os.startsWith("Mac OS")) {
            imJArea.put(KeyStroke.getKeyStroke(KeyEvent.VK_C, KeyEvent.META_DOWN_MASK), DefaultEditorKit.copyAction)
            imJArea.put(KeyStroke.getKeyStroke(KeyEvent.VK_V, KeyEvent.META_DOWN_MASK), DefaultEditorKit.pasteAction)
            imJArea.put(KeyStroke.getKeyStroke(KeyEvent.VK_X, KeyEvent.META_DOWN_MASK), DefaultEditorKit.cutAction)
            imJArea.put(KeyStroke.getKeyStroke(KeyEvent.VK_A, KeyEvent.META_DOWN_MASK), DefaultEditorKit.selectAllAction)
            imJField.put(KeyStroke.getKeyStroke(KeyEvent.VK_C, KeyEvent.META_DOWN_MASK), DefaultEditorKit.copyAction)
            imJField.put(KeyStroke.getKeyStroke(KeyEvent.VK_V, KeyEvent.META_DOWN_MASK), DefaultEditorKit.pasteAction)
            imJField.put(KeyStroke.getKeyStroke(KeyEvent.VK_X, KeyEvent.META_DOWN_MASK), DefaultEditorKit.cutAction)
            imJField.put(KeyStroke.getKeyStroke(KeyEvent.VK_A, KeyEvent.META_DOWN_MASK), DefaultEditorKit.selectAllAction)
        }
        title="CTFCrackTools$Version$Note"
        defaultCloseOperation=EXIT_ON_CLOSE
        setBounds(100, 100, 906, 755)
        contentPane=JPanel()
        contentPane.border=EmptyBorder(5, 5, 5, 5)
        setContentPane(contentPane)
        contentPane.layout=BorderLayout()
        val panel=JPanel()
        panel.addContainerListener(object : ContainerAdapter() {
            override fun componentRemoved(arg0: ContainerEvent?) {}
        })
        val model=DefaultListModel<String>()
        val addPlugins=JMenuItem("AddPlugins")
        val Tmodel=DefaultListModel<String>()
        val TaddPlugins=JMenuItem("AddPlugins")
        val topmenu=JMenuBar()
        contentPane.add(topmenu, BorderLayout.NORTH)
        contentPane.add(panel, BorderLayout.CENTER)
        val gbl_panel=GridBagLayout()
        gbl_panel.columnWidths=intArrayOf(0, 0)
        gbl_panel.rowHeights=intArrayOf(0, 0)
        gbl_panel.columnWeights=doubleArrayOf(1.0, Double.MIN_VALUE)
        gbl_panel.rowWeights=doubleArrayOf(1.0, Double.MIN_VALUE)
        panel.layout=gbl_panel
        val tabbedPane=JTabbedPane(JTabbedPane.TOP)
        val gbc_tabbedPane=GridBagConstraints()
        gbc_tabbedPane.fill=GridBagConstraints.BOTH
        gbc_tabbedPane.gridheight=0
        gbc_tabbedPane.gridx=0
        gbc_tabbedPane.gridy=0
        panel.add(tabbedPane, gbc_tabbedPane)

        val Crypto=JTabbedPane(JTabbedPane.TOP)
        Crypto.addChangeListener { textArea=(Crypto.selectedComponent as JScrollPane).viewport.view as JTextArea }
        tabbedPane.addTab("Crypto", null, Crypto, null)

        val scroll0=JScrollPane()
        val Item0=JTextArea()
        Item0.lineWrap=true
        scroll0.setViewportView(Item0)
        Item0.font=Font("新宋体", Font.PLAIN, 13)
        Item0.text="Author:0chen\r\nTeam:MstTeam\r\n"+
                "Website:http://www.Hi-OurLife.com/\r\n"+
                "Github:https://github.com/0Chencc/CTFCrackTools\r\n"+
                "GitPage:https://0chencc.github.io/CTFCrackTools/\r\n\r\n" +
                "本框架支持4种主题，请于Setting中的Theme中修改，分别为1/2/3，什么都不填或者填写其他，会用默认主题\r\n" +
                "主题1，需要在JDK8以及以下版本使用，不兼容JDK9、JDK10\r\n" +
                "值得注意的是，之前插件保存的JSON文件是Setting.json，但是本次更新将更换为Plugins.json\r\n" +
                "请各位使用之前版本的朋友，将原来的Setting.json重命名为Plugins.json"
        Crypto.addTab("0", null, scroll0, null)

        val scroll1=JScrollPane()
        Crypto.addTab("1", null, scroll1, null)

        val Item1=JTextArea()
        Item1.lineWrap=true
        Item1.font=Font("新宋体", Font.PLAIN, 13)
        scroll1.setViewportView(Item1)

        val scroll2=JScrollPane()
        Crypto.addTab("2", null, scroll2, null)

        val Item2=JTextArea()
        Item2.lineWrap=true
        Item2.font=Font("新宋体", Font.PLAIN, 13)
        scroll2.setViewportView(Item2)

        val scroll3=JScrollPane()
        Crypto.addTab("3", null, scroll3, null)

        val Item3=JTextArea()
        Item3.lineWrap=true
        Item3.font=Font("新宋体", Font.PLAIN, 13)
        scroll3.setViewportView(Item3)

        val scroll4=JScrollPane()
        Crypto.addTab("4", null, scroll4, null)
        val Item4=JTextArea()
        Item4.lineWrap=true
        Item4.font=Font("新宋体", Font.PLAIN, 13)
        scroll4.setViewportView(Item4)

        val scroll5=JScrollPane()
        Crypto.addTab("5", null, scroll5, null)

        val Item5=JTextArea()
        Item5.lineWrap=true
        Item5.font=Font("新宋体", Font.PLAIN, 13)
        scroll5.setViewportView(Item5)

        val scroll6=JScrollPane()
        Crypto.addTab("6", null, scroll6, null)

        val Item6=JTextArea()
        Item6.lineWrap=true
        Item6.font=Font("新宋体", Font.PLAIN, 13)
        scroll6.setViewportView(Item6)

        val scroll7=JScrollPane()
        Crypto.addTab("7", null, scroll7, null)

        val Item7=JTextArea()
        Item7.lineWrap=true
        Item7.font=Font("新宋体", Font.PLAIN, 13)
        scroll7.setViewportView(Item7)

        val scroll8=JScrollPane()
        Crypto.addTab("8", null, scroll8, null)

        val Item8=JTextArea()
        Item8.lineWrap=true
        Item8.font=Font("新宋体", Font.PLAIN, 13)
        scroll8.setViewportView(Item8)

        val scroll9=JScrollPane()
        Crypto.addTab("9", null, scroll9, null)

        val Item9=JTextArea()
        Item9.lineWrap=true
        Item9.font=Font("新宋体", Font.PLAIN, 13)
        scroll9.setViewportView(Item9)
        /* Double Click to copy-双击复制
        Item0.addMouseListener(object:MouseAdapter(){
            override fun mouseClicked(e: MouseEvent?) {
                if(e!!.clickCount==2){
                    textArea.paste()
                }
            }
        })*/
        val menu=JPopupMenu()

        addPopup(Item0, menu)
        addPopup(Item1, menu)
        addPopup(Item2, menu)
        addPopup(Item3, menu)
        addPopup(Item4, menu)
        addPopup(Item5, menu)
        addPopup(Item6, menu)
        addPopup(Item7, menu)
        addPopup(Item8, menu)
        addPopup(Item9, menu)
        //PopupMenu
        val Decrypt=JMenu("Decrypt")
        menu.add(Decrypt)
        val CaesarCode=JMenuItem("CaesarCode")
        CaesarCode.addActionListener { textArea.text=f.Caesar(textArea.text) }
        Decrypt.add(CaesarCode)
        val Rot13=JMenuItem("Rot13")
        Rot13.addActionListener { textArea.text=f.Rot13(textArea.text) }
        Decrypt.add(Rot13)
        val Fencecode=JMenuItem("FenceCode")
        Fencecode.addActionListener { textArea.text=f.Fence(textArea.text) }
        Decrypt.add(Fencecode)
        val Pigcode=JMenuItem("PigCode")
        Pigcode.addActionListener { textArea.text=f.PigCode(textArea.text) }
        Decrypt.add(Pigcode)
        val Reverse=JMenuItem("Reverse")
        Reverse.addActionListener { textArea.text=f.reverse(textArea.text) }
        Decrypt.add(Reverse)
        val Ascii2Hex=JMenuItem("Ascii->Hex")
        Ascii2Hex.addActionListener { textArea.text=f.StringtoHex(textArea.text) }
        Decrypt.add(Ascii2Hex)
        val Hex2Ascii=JMenuItem("Hex->Ascii")
        Hex2Ascii.addActionListener { textArea.text=f.HextoString(textArea.text) }
        Decrypt.add(Hex2Ascii)
        val Ascii2Unicode=JMenuItem("Ascii->Unicode")
        Ascii2Unicode.addActionListener { textArea.text=f.AsciiToUnicode(textArea.text) }
        Decrypt.add(Ascii2Unicode)
        val Unicode2Ascii=JMenuItem("Unicode->Ascii")
        Unicode2Ascii.addActionListener { textArea.text=f.UnicodeToAscii(textArea.text) }
        Decrypt.add(Unicode2Ascii)

        val Decode=JMenu("Decode")
        menu.add(Decode)
        val Base64Decode=JMenuItem("Base64DeCode")
        Base64Decode.addActionListener { textArea.text=f.Base64de(textArea.text) }
        Decode.add(Base64Decode)
        val Base32Decode=JMenuItem("Base32DeCode")
        Base32Decode.addActionListener { textArea.text=f.Base32de(textArea.text) }
        Decode.add(Base32Decode)
        /*
        JMenuItem Base16Decode = new JMenuItem("Base16Decode");
        Base16Decode.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                textArea.setText(f.Base16de(textArea.getText()));
            }
        });
        Decode.add(Base16Decode);*/
        val MorseDecode=JMenuItem("MorseDeCode")
        MorseDecode.addActionListener { textArea.text=f.MorseDecode(textArea.text) }
        Decode.add(MorseDecode)
        val BaconDecode=JMenuItem("BaconDeCode")
        BaconDecode.addActionListener { textArea.text=f.BaconCodeDecode(textArea.text) }
        Decode.add(BaconDecode)
        val UrlDecode=JMenuItem("UrlDeCode")
        UrlDecode.addActionListener { textArea.text=f.URLDecoder(textArea.text) }
        Decode.add(UrlDecode)
        val UniDecode=JMenuItem("UnicodeDeCode")
        UniDecode.addActionListener { textArea.text=f.UnicodeDecode(textArea.text) }
        Decode.add(UniDecode)
        val VigenereDecode=JMenuItem("VigenereDeCode")
        VigenereDecode.addActionListener{textArea.text=f.VigenereDeCode(textArea.text.toCharArray(),JOptionPane.showInputDialog("Please input a key").toCharArray())}
        Decode.add(VigenereDecode)
        val HtmlEDe=JMenuItem("Html Entity DeCode")
        HtmlEDe.addActionListener{textArea.text=StringEscapeUtils.unescapeHtml4(textArea.text)}
        Decode.add(HtmlEDe)
        //Encode
        val Encode=JMenu("Encode")
        menu.add(Encode)
        /*        JMenuItem Base64Encodegbk = new JMenuItem("Base64EncodeGBK");
        Base64Encodegbk.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                textArea.setText(f.Base64en(textArea.getText()));
            }
        });
        Encode.add(Base64Encodegbk);*/
        val Base32Encode=JMenuItem("Base32Encode")
        Base32Encode.addActionListener { textArea.text=f.Base32en(textArea.text) }
        val Base64Encode=JMenuItem("Base64Encode")
        Base64Encode.addActionListener { textArea.text=f.Base64en(textArea.text) }
        Encode.add(Base64Encode)
        Encode.add(Base32Encode)
        /*        JMenuItem Base16Encode = new JMenuItem("Base16Encode");
        Base16Encode.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                textArea.setText(f.Base16en(textArea.getText()));
            }
        });
        Encode.add(Base16Encode);*/

        val MorseEncode=JMenuItem("MorseEnCode")
        MorseEncode.addActionListener { textArea.text=f.MorseEncode(textArea.text) }
        Encode.add(MorseEncode)

        val BaconEncode=JMenuItem("BaconEnCode")
        BaconEncode.addActionListener { textArea.text=f.BaconCodeEncode(textArea.text) }
        Encode.add(BaconEncode)

        val UrlEncode=JMenuItem("UrlEnCode")
        UrlEncode.addActionListener { textArea.text=f.UrlEncoder(textArea.text) }
        Encode.add(UrlEncode)

        val UnicodeEncode=JMenuItem("UnicodeEnCode")
        UnicodeEncode.addActionListener { textArea.text=f.UnicodeEncode(textArea.text) }
        Encode.add(UnicodeEncode)
        val VigenereEncode=JMenuItem("VigenereEnCode")
        VigenereEncode.addActionListener{textArea.text=f.VigenereEnCode(textArea.text.toCharArray(),JOptionPane.showInputDialog("Please input a key").toCharArray())}
        Encode.add(VigenereEncode)
        val HtmlEEn=JMenuItem("Html Entity EnCode")
        HtmlEEn.addActionListener{textArea.text=StringEscapeUtils.escapeHtml4(textArea.text)}
        Encode.add(HtmlEEn)

        val Plugins=JMenu("Plugins")
        menu.add(Plugins)


        //TopMenu
        val topDec=JMenu("Decrypt")
        topmenu.add(topDec)
        val TCaesar=JMenuItem("CaesarCode")
        TCaesar.addActionListener { textArea.text=f.Caesar(textArea.text) }
        topDec.add(TCaesar)
        val TRot13=JMenuItem("Rot13")
        TRot13.addActionListener { textArea.text=f.Rot13(textArea.text) }
        topDec.add(TRot13)
        val TFencecode=JMenuItem("FenceCode")
        TFencecode.addActionListener { textArea.text=f.Fence(textArea.text) }
        topDec.add(TFencecode)
        val TPigcode=JMenuItem("PigCode")
        TPigcode.addActionListener { textArea.text=f.PigCode(textArea.text) }
        topDec.add(TPigcode)
        val TReverse=JMenuItem("Reverse")
        TReverse.addActionListener { textArea.text=f.reverse(textArea.text) }
        topDec.add(TReverse)
        val TAscii2Hex=JMenuItem("Ascii->Hex")
        TAscii2Hex.addActionListener { textArea.text=f.StringtoHex(textArea.text) }
        topDec.add(TAscii2Hex)
        val THex2Ascii=JMenuItem("Hex->Ascii")
        THex2Ascii.addActionListener { textArea.text=f.HextoString(textArea.text) }
        topDec.add(THex2Ascii)
        val TAscii2Unicode=JMenuItem("Ascii->Unicode")
        TAscii2Unicode.addActionListener { textArea.text=f.AsciiToUnicode(textArea.text) }
        topDec.add(TAscii2Unicode)
        val TUnicode2Ascii=JMenuItem("Unicode->Ascii")
        TUnicode2Ascii.addActionListener { textArea.text=f.UnicodeToAscii(textArea.text) }
        topDec.add(TUnicode2Ascii)

        val TDecode=JMenu("Decode")
        topmenu.add(TDecode)
        val TBase64DecodeUTF8=JMenuItem("Base64DeCode")
        TBase64DecodeUTF8.addActionListener { textArea.text=f.Base64de(textArea.text) }
        TDecode.add(TBase64DecodeUTF8)
        val TBase32Decode=JMenuItem("Base32DeCode")
        TBase32Decode.addActionListener { textArea.text=f.Base32de(textArea.text) }
        TDecode.add(TBase32Decode)
        val TMorseDecode=JMenuItem("MorseDeCode")
        TMorseDecode.addActionListener { textArea.text=f.MorseDecode(textArea.text) }
        TDecode.add(TMorseDecode)
        val TBaconDecode=JMenuItem("BaconDeCode")
        TBaconDecode.addActionListener { textArea.text=f.BaconCodeDecode(textArea.text) }
        TDecode.add(TBaconDecode)
        val TUrlDecode=JMenuItem("UrlDeCode")
        TUrlDecode.addActionListener { textArea.text=f.URLDecoder(textArea.text) }
        TDecode.add(TUrlDecode)
        val TUniDecode=JMenuItem("UnicodeDeCode")
        TUniDecode.addActionListener { textArea.text=f.UnicodeDecode(textArea.text) }
        TDecode.add(TUniDecode)
        val TVigenereDecode=JMenuItem("VigenereDeCode")
        TVigenereDecode.addActionListener{textArea.text=f.VigenereDeCode(textArea.text.toCharArray(),JOptionPane.showInputDialog("Please input a key").toCharArray())}
        TDecode.add(TVigenereDecode)

        val TEncode=JMenu("Encode")
        topmenu.add(TEncode)
        val TBase64Encode=JMenuItem("Base64EnCode")
        TBase64Encode.addActionListener { textArea.text=f.Base64en(textArea.text) }
        TEncode.add(TBase64Encode)
        val TBase32Encode=JMenuItem("Base32EnCode")
        TBase32Encode.addActionListener { textArea.text=f.Base32en(textArea.text) }
        TEncode.add(TBase32Encode)
        val TMorseEncode=JMenuItem("MorseEnCode")
        TMorseEncode.addActionListener { textArea.text=f.MorseEncode(textArea.text) }
        TEncode.add(TMorseEncode)
        val TBaconEncode=JMenuItem("BaconEnCode")
        TBaconEncode.addActionListener { textArea.text=f.BaconCodeEncode(textArea.text) }
        TEncode.add(TBaconEncode)
        val TUrlEncode=JMenuItem("UrlEnCode")
        TUrlEncode.addActionListener { textArea.text=f.UrlEncoder(textArea.text) }
        TEncode.add(TUrlEncode)
        val TUnicodeEncode=JMenuItem("UnicodeEnCode")
        TUnicodeEncode.addActionListener { textArea.text=f.UnicodeEncode(textArea.text) }
        TEncode.add(TUnicodeEncode)
        val TVigenereEncode=JMenuItem("VigenereEnCode")
        TVigenereEncode.addActionListener{textArea.text=f.VigenereEnCode(textArea.text.toCharArray(),JOptionPane.showInputDialog("Please input a key").toCharArray())}
        TEncode.add(TVigenereEncode)

        val TPlugins=JMenu("Plugins")
        topmenu.add(TPlugins)
        /* addPluginEvent */
        addPlugins.addActionListener {
            val py_suf=arrayOf("py")
            val py_filter: FileNameExtensionFilter
            val py_openfile=JFileChooser()
            py_openfile.fileSelectionMode=JFileChooser.FILES_ONLY
            py_filter=FileNameExtensionFilter("Python(.py)", *py_suf)
            py_openfile.fileFilter=py_filter
            val py_openframe=py_openfile.showDialog(JLabel(), "选择/Choose")
            if(py_openframe==JFileChooser.APPROVE_OPTION) {
                val py_file=py_openfile.selectedFile//得到选择的文件名
                try {
                    val title=json.createJSON(py_file.toString())
                    when (json.search(title,"type")) {
                        "crypto" -> {
                            Plugins.add(buildPluginMenuItem(title))
                            TPlugins.add(buildPluginMenuItem(title))
                        }
                    }
                    model.addElement(title)
                    Tmodel.addElement(title)
                } catch (e1: IOException) {
                    e1.printStackTrace()
                } catch (e1: Exception) {
                    // TODO 自动生成的 catch 块
                    e1.printStackTrace()
                }

            }
        }
        Plugins.add(addPlugins)
        try {
            buildCryptoPlugin(Plugins)
        } catch (e1: Exception) {
            // TODO 自动生成的 catch 块
            e1.printStackTrace()
        }
        TaddPlugins.addActionListener {
            val py_suf=arrayOf("py")
            val py_filter: FileNameExtensionFilter
            val py_openfile=JFileChooser()
            py_openfile.fileSelectionMode=JFileChooser.FILES_ONLY
            py_filter=FileNameExtensionFilter("Python(.py)", *py_suf)
            py_openfile.fileFilter=py_filter
            val py_openframe=py_openfile.showDialog(JLabel(), "选择/Choose")
            if(py_openframe==JFileChooser.APPROVE_OPTION) {
                val py_file=py_openfile.selectedFile//得到选择的文件名
                try {
                    val title=json.createJSON(py_file.toString())
                    when (json.search(title,"type")) {
                        "crypto" -> {
                            Plugins.add(buildPluginMenuItem(title))
                            Plugins.add(buildPluginMenuItem(title))
                        }
                    }
                    Tmodel.addElement(title)
                    model.addElement(title)
                } catch (e1: IOException) {
                    e1.printStackTrace()
                } catch (e1: Exception) {
                    // TODO 自动生成的 catch 块
                    e1.printStackTrace()
                }

            }
        }
        TPlugins.add(TaddPlugins)
        try {
            buildCryptoPlugin(TPlugins)
        } catch (e1: Exception) {
            // TODO 自动生成的 catch 块
            e1.printStackTrace()
        }

        val HexConvert=JPanel()
        tabbedPane.addTab("HexConvert", null, HexConvert, null)
        val gbl_HexConvert=GridBagLayout()
        gbl_HexConvert.columnWidths=intArrayOf(59, 533, 0)
        gbl_HexConvert.rowHeights=intArrayOf(0, 0, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 0)
        gbl_HexConvert.columnWeights=doubleArrayOf(1.0, 1.0, Double.MIN_VALUE)
        gbl_HexConvert.rowWeights=doubleArrayOf(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE)
        HexConvert.layout=gbl_HexConvert

        val comboBox=JComboBox<String>()
        comboBox.setModel(DefaultComboBoxModel(arrayOf("Binary", "Octal", "Decimal", "Hexadecimal", "32Hexadecimal", "36Hexadecimal")))
        val gbc_comboBox=GridBagConstraints()
        gbc_comboBox.insets=Insets(0, 0, 5, 5)
        gbc_comboBox.fill=GridBagConstraints.HORIZONTAL
        gbc_comboBox.gridx=0
        gbc_comboBox.gridy=0
        HexConvert.add(comboBox, gbc_comboBox)

        inputnum=JTextField()
        val gbc_inputnum=GridBagConstraints()
        gbc_inputnum.insets=Insets(0, 0, 5, 0)
        gbc_inputnum.fill=GridBagConstraints.HORIZONTAL
        gbc_inputnum.gridx=1
        gbc_inputnum.gridy=0
        HexConvert.add(inputnum, gbc_inputnum)
        inputnum.columns=10

        val lblNewLabel_7=JLabel("HexConvert:2/8/10/16/32/36")
        val gbc_lblNewLabel_7=GridBagConstraints()
        gbc_lblNewLabel_7.insets=Insets(0, 0, 5, 5)
        gbc_lblNewLabel_7.gridx=0
        gbc_lblNewLabel_7.gridy=1
        HexConvert.add(lblNewLabel_7, gbc_lblNewLabel_7)

        val lblNewLabel=JLabel("Result")
        val gbc_lblNewLabel=GridBagConstraints()
        gbc_lblNewLabel.insets=Insets(0, 0, 5, 0)
        gbc_lblNewLabel.gridx=1
        gbc_lblNewLabel.gridy=1
        HexConvert.add(lblNewLabel, gbc_lblNewLabel)

        val lblNewLabel_1=JLabel("Binary")
        val gbc_lblNewLabel_1=GridBagConstraints()
        gbc_lblNewLabel_1.gridheight=2
        gbc_lblNewLabel_1.anchor=GridBagConstraints.ABOVE_BASELINE
        gbc_lblNewLabel_1.insets=Insets(0, 0, 5, 5)
        gbc_lblNewLabel_1.gridx=0
        gbc_lblNewLabel_1.gridy=2
        HexConvert.add(lblNewLabel_1, gbc_lblNewLabel_1)

        hex2=JTextField()
        hex8=JTextField()
        hex10=JTextField()
        hex16=JTextField()
        hex32=JTextField()
        hex36=JTextField()

        inputnum.addCaretListener {
            if(inputnum.text!="") {
                var input=inputnum.text
                input=input.replace(" ", "")
                var radixnum=10
                when (comboBox.getSelectedItem()!!.toString()) {
                    "Binary" -> radixnum=2
                    "Octal" -> radixnum=8
                    "Decimal" -> radixnum=10
                    "Hexadecimal" -> radixnum=16
                    "32Hexadecimal" -> radixnum=32
                    "36Hexadecimal" -> radixnum=36
                    else -> {
                    }
                }
                hex2.text=BigInteger(input, radixnum).toString(2)
                hex8.text=BigInteger(input, radixnum).toString(8)
                hex10.text=BigInteger(input, radixnum).toString(10)
                hex16.text=BigInteger(input, radixnum).toString(16)
                hex32.text=BigInteger(input, radixnum).toString(32)
                hex36.text=BigInteger(input, radixnum).toString(36)
            } else {
                hex2.text=""
                hex8.text=""
                hex10.text=""
                hex16.text=""
                hex32.text=""
                hex36.text=""
            }
        }
        val gbc_hex2=GridBagConstraints()
        gbc_hex2.gridheight=2
        gbc_hex2.fill=GridBagConstraints.HORIZONTAL
        gbc_hex2.insets=Insets(0, 0, 5, 0)
        gbc_hex2.gridx=1
        gbc_hex2.gridy=2
        HexConvert.add(hex2, gbc_hex2)
        hex2.columns=10

        val lblNewLabel_2=JLabel("Octal")
        val gbc_lblNewLabel_2=GridBagConstraints()
        gbc_lblNewLabel_2.gridheight=2
        gbc_lblNewLabel_2.insets=Insets(0, 0, 5, 5)
        gbc_lblNewLabel_2.gridx=0
        gbc_lblNewLabel_2.gridy=4
        HexConvert.add(lblNewLabel_2, gbc_lblNewLabel_2)
        val gbc_hex8=GridBagConstraints()
        gbc_hex8.gridheight=2
        gbc_hex8.fill=GridBagConstraints.HORIZONTAL
        gbc_hex8.insets=Insets(0, 0, 5, 0)
        gbc_hex8.gridx=1
        gbc_hex8.gridy=4
        HexConvert.add(hex8, gbc_hex8)
        hex8.columns=10

        val lblNewLabel_3=JLabel("Decimal")
        val gbc_lblNewLabel_3=GridBagConstraints()
        gbc_lblNewLabel_3.gridheight=2
        gbc_lblNewLabel_3.insets=Insets(0, 0, 5, 5)
        gbc_lblNewLabel_3.gridx=0
        gbc_lblNewLabel_3.gridy=6
        HexConvert.add(lblNewLabel_3, gbc_lblNewLabel_3)
        val gbc_hex10=GridBagConstraints()
        gbc_hex10.gridheight=2
        gbc_hex10.fill=GridBagConstraints.HORIZONTAL
        gbc_hex10.insets=Insets(0, 0, 5, 0)
        gbc_hex10.gridx=1
        gbc_hex10.gridy=6
        HexConvert.add(hex10, gbc_hex10)
        hex10.columns=10

        val lblNewLabel_4=JLabel("Hexadecimal")
        val gbc_lblNewLabel_4=GridBagConstraints()
        gbc_lblNewLabel_4.gridheight=2
        gbc_lblNewLabel_4.insets=Insets(0, 0, 5, 5)
        gbc_lblNewLabel_4.gridx=0
        gbc_lblNewLabel_4.gridy=8
        HexConvert.add(lblNewLabel_4, gbc_lblNewLabel_4)

        val gbc_hex16=GridBagConstraints()
        gbc_hex16.gridheight=2
        gbc_hex16.fill=GridBagConstraints.HORIZONTAL
        gbc_hex16.insets=Insets(0, 0, 5, 0)
        gbc_hex16.gridx=1
        gbc_hex16.gridy=8
        HexConvert.add(hex16, gbc_hex16)
        hex16.columns=10

        val lblNewLabel_5=JLabel("32Hexadecimal")
        val gbc_lblNewLabel_5=GridBagConstraints()
        gbc_lblNewLabel_5.gridheight=2
        gbc_lblNewLabel_5.insets=Insets(0, 0, 5, 5)
        gbc_lblNewLabel_5.gridx=0
        gbc_lblNewLabel_5.gridy=10
        HexConvert.add(lblNewLabel_5, gbc_lblNewLabel_5)

        val gbc_hex32=GridBagConstraints()
        gbc_hex32.gridheight=2
        gbc_hex32.fill=GridBagConstraints.HORIZONTAL
        gbc_hex32.insets=Insets(0, 0, 5, 0)
        gbc_hex32.gridx=1
        gbc_hex32.gridy=10
        HexConvert.add(hex32, gbc_hex32)
        hex32.columns=10

        val lblNewLabel_6=JLabel("36Hexadecimal")
        val gbc_lblNewLabel_6=GridBagConstraints()
        gbc_lblNewLabel_6.gridheight=2
        gbc_lblNewLabel_6.insets=Insets(0, 0, 0, 5)
        gbc_lblNewLabel_6.gridx=0
        gbc_lblNewLabel_6.gridy=12
        HexConvert.add(lblNewLabel_6, gbc_lblNewLabel_6)

        val gbc_hex36=GridBagConstraints()
        gbc_hex36.gridheight=2
        gbc_hex36.fill=GridBagConstraints.HORIZONTAL
        gbc_hex36.gridx=1
        gbc_hex36.gridy=12
        HexConvert.add(hex36, gbc_hex36)
        hex36.columns=10
        val PluginsMenu=JPanel()
        tabbedPane.addTab("PluginsMenu", null, PluginsMenu, null)
        val gbl_PluginsMenu=GridBagLayout()
        gbl_PluginsMenu.columnWidths=intArrayOf(257, 7, 279, 0)
        gbl_PluginsMenu.rowHeights=intArrayOf(0, 0, 0)
        gbl_PluginsMenu.columnWeights=doubleArrayOf(1.0, 1.0, 1.0, Double.MIN_VALUE)
        gbl_PluginsMenu.rowWeights=doubleArrayOf(0.0, 1.0, Double.MIN_VALUE)
        PluginsMenu.layout=gbl_PluginsMenu

        val PluginsList=JLabel("PluginsList")
        val gbc_PluginsList=GridBagConstraints()
        gbc_PluginsList.insets=Insets(0, 0, 5, 5)
        gbc_PluginsList.gridx=0
        gbc_PluginsList.gridy=0
        PluginsMenu.add(PluginsList, gbc_PluginsList)

        val PluginDetaillb=JLabel("PluginDetail")
        val gbc_PluginDetaillb=GridBagConstraints()
        gbc_PluginDetaillb.insets=Insets(0, 0, 5, 0)
        gbc_PluginDetaillb.gridx=2
        gbc_PluginDetaillb.gridy=0
        PluginsMenu.add(PluginDetaillb, gbc_PluginDetaillb)


        val scrollPane=JScrollPane()
        val gbc_scrollPane=GridBagConstraints()
        gbc_scrollPane.fill=GridBagConstraints.BOTH
        gbc_scrollPane.gridx=2
        gbc_scrollPane.gridy=1
        PluginsMenu.add(scrollPane, gbc_scrollPane)

        val PluginDetail=JTextArea()
        PluginDetail.font=Font("新宋体", Font.PLAIN, 13)
        scrollPane.setViewportView(PluginDetail)

        try {
            buildPluginMenu(model)
            buildPluginMenu(Tmodel)
        } catch (e1: Exception) {
            // TODO 自动生成的 catch 块
            e1.printStackTrace()
        }

        val list=JList(model)
        list.border=LineBorder(Color.LIGHT_GRAY)
        list.foreground=Color.BLACK
        list.background=Color.WHITE
        list.addMouseListener(object : MouseAdapter() {
            override fun mouseClicked(arg0: MouseEvent?) {
                try {
                    PluginDetail.text=json.getDetail(list.selectedValue)
                } catch (e: Exception) {
                    // TODO 自动生成的 catch 块
                    e.printStackTrace()
                }

            }
        })

        val gbc_list=GridBagConstraints()
        gbc_list.insets=Insets(0, 0, 0, 5)
        gbc_list.fill=GridBagConstraints.BOTH
        gbc_list.gridx=0
        gbc_list.gridy=1
        PluginsMenu.add(list, gbc_list)

        val panel_1=JPanel()
        val gbc_panel_1=GridBagConstraints()
        gbc_panel_1.insets=Insets(0, 0, 0, 5)
        gbc_panel_1.fill=GridBagConstraints.VERTICAL
        gbc_panel_1.gridx=1
        gbc_panel_1.gridy=1
        PluginsMenu.add(panel_1, gbc_panel_1)
        val gbl_panel_1=GridBagLayout()
        gbl_panel_1.columnWidths=intArrayOf(69, 0)
        gbl_panel_1.rowHeights=intArrayOf(180, 23, 35, 23, 0)
        gbl_panel_1.columnWeights=doubleArrayOf(0.0, Double.MIN_VALUE)
        gbl_panel_1.rowWeights=doubleArrayOf(0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE)
        panel_1.layout=gbl_panel_1
        //删除插件
        val RemovePlugin=JButton("Remove")
        RemovePlugin.addActionListener {
            try {
                val rmPlugin=list.selectedValue
                when (json.search(rmPlugin,"type")) {
                    "crypto" -> for (i in 0..Plugins.itemCount) {
                        if(Plugins.getItem(i).label.equals(rmPlugin, ignoreCase=true)) {
                            Plugins.remove(i)
                            TPlugins.remove(i)
                            break
                        }
                    }
                }
                model.removeElement(rmPlugin)
                Tmodel.removeElement(rmPlugin)
                json.rmPlugin(rmPlugin)
                PluginDetail.text=""
            } catch (e: Exception) {
                // TODO 自动生成的 catch 块
                e.printStackTrace()
            }
        }
        //添加插件addPlugin
        val AddPlugin=JButton("Append")
        AddPlugin.addActionListener {
            val py_suf=arrayOf("py")
            val py_filter: FileNameExtensionFilter
            val py_openfile=JFileChooser()
            py_openfile.fileSelectionMode=JFileChooser.FILES_ONLY
            py_filter=FileNameExtensionFilter("Python(.py)", *py_suf)
            py_openfile.fileFilter=py_filter
            val py_openframe=py_openfile.showDialog(JLabel(), "选择/Choose")
            if(py_openframe==JFileChooser.APPROVE_OPTION) {
                val py_file=py_openfile.selectedFile//得到选择的文件名
                try {
                    val title=json.createJSON(py_file.toString())
                    when (json.search(title,"type")) {
                        "crypto" -> {
                            TPlugins.add(buildPluginMenuItem(title))
                            Plugins.add(buildPluginMenuItem(title))
                        }
                    }
                    model.addElement(title)
                    Tmodel.addElement(title)
                } catch (e1: IOException) {
                    e1.printStackTrace()
                } catch (e1: Exception) {
                    e1.printStackTrace()
                }

            }
        }
        val gbc_AddPlugin=GridBagConstraints()
        gbc_AddPlugin.insets=Insets(0, 0, 5, 0)
        gbc_AddPlugin.gridx=0
        gbc_AddPlugin.gridy=1
        panel_1.add(AddPlugin, gbc_AddPlugin)
        RemovePlugin.horizontalAlignment=SwingConstants.LEADING
        val gbc_RemovePlugin=GridBagConstraints()
        gbc_RemovePlugin.gridx=0
        gbc_RemovePlugin.gridy=3
        panel_1.add(RemovePlugin, gbc_RemovePlugin)
    }

    @Throws(Exception::class)
    private fun buildPluginMenu(pluginlist: DefaultListModel<String>) {
        if(File(PluginsJsonPath).isFile() && File(PluginsJsonPath).exists() && json.isJSON(PluginsJsonPath)) {
            val jsonfile=FileInputStream(PluginsJsonPath)
            val jsonreadcoding=InputStreamReader(jsonfile, "UTF-8")
            val parser=JsonParser()
            val `object`=parser.parse(BufferedReader(jsonreadcoding)) as JsonObject
            val Plugins=`object`.getAsJsonArray("Plugins")
            if(Plugins!=null){
                for (jsonElement in Plugins) {
                    val Plugin=jsonElement.asJsonObject
                    pluginlist.addElement(Plugin.get("title").asString)
                }
            }
        }
    }

    @Throws(Exception::class)
    private fun buildCryptoPlugin(menu: JMenu) {
        if(File(PluginsJsonPath).isFile() && File(PluginsJsonPath).exists() && json.isJSON(PluginsJsonPath)) {
            val jsonfile=FileInputStream(PluginsJsonPath)
            val jsonreadcoding=InputStreamReader(jsonfile, "UTF-8")
            val parser=JsonParser()
            val `object`=parser.parse(BufferedReader(jsonreadcoding)) as JsonObject
            val Plugins=`object`.getAsJsonArray("Plugins")
            if(Plugins!=null){
                for (jsonElement in Plugins) {
                    val Plugin=jsonElement.asJsonObject
                    if(Plugin.get("type").asString.toLowerCase().equals("crypto", ignoreCase=true)) {
                        menu.add(buildPluginMenuItem(Plugin.get("title").asString))
                    }
                }
            }
        }
    }

    @Throws(Exception::class)
    fun buildPluginMenuItem(filename: String): JMenuItem {
        val item=JMenuItem(filename)
        item.actionCommand=filename
        item.addActionListener { arg0 ->
            val input=textArea.text
            val props=Properties()
            props["python.home"]=System.getProperty("user.dir")+"/Lib"
            props["python.console.encoding"]="UTF-8"
            props["python.security.respectJavaAccessibility"]="false"
            props["python.import.site"]="false"
            val preprops=System.getProperties()
            PythonInterpreter.initialize(preprops, props, arrayOfNulls(0))
            val interpreter=PythonInterpreter()
            val sys=Py.getSystemState()
            sys.path.add(System.getProperty("user.dir")+"/Lib/site-packages")
            //sys.path.add("C:/Python27/Lib/site-packages")
            try {
                interpreter.execfile(json.search(arg0.actionCommand,"path"))
            } catch (e: Exception) {
                e.printStackTrace()
            }

            var dialog: Array<String>?=null
            var dialogstr: String?=null
            var f: PyFunction?=null
            var res: PyObject?=null
            try {
                if(json.isDialog(arg0.actionCommand)) {
                    dialogstr=json.search(arg0.actionCommand,"dialog")
                    dialog=dialogstr!!.split(",".toRegex()).dropLastWhile { it.isEmpty() }.toTypedArray()
                    when (dialog.size) {
                        3 -> {
                            dialog[0]=JOptionPane.showInputDialog("Please input a "+dialog[0])
                            dialog[1]=JOptionPane.showInputDialog("Please input a "+dialog[1])
                            dialog[2]=JOptionPane.showInputDialog("Please input a "+dialog[2])
                            f=interpreter.get("main", PyFunction::class.java) as PyFunction
                            res=f.__call__(PyString(input), PyString(dialog[0]), PyString(dialog[1]), PyString(dialog[2]))
                            textArea.text=res!!.toString()
                        }
                        2 -> {
                            dialog[0]=JOptionPane.showInputDialog("Please input a "+dialog[0])
                            dialog[1]=JOptionPane.showInputDialog("Please input a "+dialog[1])
                            f=interpreter.get("main", PyFunction::class.java) as PyFunction
                            res=f.__call__(PyString(input), PyString(dialog[0]), PyString(dialog[1]))
                            textArea.text=res!!.toString()
                        }
                        1 -> {
                            dialog[0]=JOptionPane.showInputDialog("Please input a "+dialog[0])
                            println(dialog[0])
                            f=interpreter.get("main", PyFunction::class.java) as PyFunction
                            res=f.__call__(PyString(input), PyString(dialog[0]))
                            textArea.text=res!!.toString()
                        }
                        else -> {
                            f=interpreter.get("main", PyFunction::class.java) as PyFunction
                            res=f.__call__(PyString(input))
                            textArea.text=res!!.toString()
                        }
                    }
                } else {
                    f=interpreter.get("main", PyFunction::class.java) as PyFunction
                    res=f.__call__(PyString(input))
                    textArea.text=res!!.toString()
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        return item
    }

    companion object {
        private var textArea=JTextArea()
        private val PluginsJsonPath=String(StringBuilder(System.getProperty("user.dir")+"/Plugins.json"))
        private val SettingJsonPath = String(StringBuilder(System.getProperty("user.dir")+"/Setting.json"))
        private val Version="-v3.2.4"
        private val Note="林晨skr憨憨"
        private val json=Json()
        private var themes: Int=0

        /**
         * Launch the application.
         */
        init {
            if(File(SettingJsonPath).isFile() && File(SettingJsonPath).exists() && json.isJSON(SettingJsonPath)) {
                val jsonfile=FileInputStream(SettingJsonPath)
                val jsonreadcoding=InputStreamReader(jsonfile, "UTF-8")
                val parser=JsonParser()
                val `object`=parser.parse(BufferedReader(jsonreadcoding)) as JsonObject
                val Themes=`object`.getAsJsonArray("Themes")
                if(Themes!=null){
                    for (jsonElement in Themes) {
                        val Theme=jsonElement.asJsonObject
                        if(Theme.toString()!="{}") {
                            when (Theme.get("Theme").asInt) {
                                1 -> {
                                    try {
                                        BeautyEyeLNFHelper.frameBorderStyle=BeautyEyeLNFHelper.FrameBorderStyle.translucencySmallShadow//外观1
                                        BeautyEyeLNFHelper.launchBeautyEyeLNF()
                                        BeautyEyeLNFHelper.translucencyAtFrameInactive=true
                                        UIManager.put("RootPane.setupButtonVisible", false)
                                    } catch (e: Exception) {
                                    }
                                }
                                2 -> {
                                    try {
                                        UIManager.setLookAndFeel(MaterialLookAndFeel())//外观2
                                    } catch (e: UnsupportedLookAndFeelException) {
                                        e.printStackTrace()
                                    }
                                }
                                3 -> {
                                    WebLookAndFeel.install()//外观3
                                }
                                else -> {

                                }
                            }
                        }
                    }

                }
            }
        }

        @JvmStatic
        fun main(args: Array<String>) {
            EventQueue.invokeLater {
                try {
                    val frame=Core()
                    frame.isVisible=true
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }

        private fun addPopup(component: Component, popup: JPopupMenu) {
            component.addMouseListener(object : MouseAdapter() {
                override fun mousePressed(e: MouseEvent?) {
                    if(e!!.isPopupTrigger) {
                        showMenu(e)
                    }
                }

                override fun mouseReleased(e: MouseEvent?) {
                    if(e!!.isPopupTrigger) {
                        showMenu(e)
                    }
                }

                private fun showMenu(e: MouseEvent) {
                    popup.show(e.component, e.x, e.y)
                }
            })
        }
    }
}