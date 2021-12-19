package org.ctfcracktools.ui;/*
 * Created by JFormDesigner on Thu Nov 25 10:28:49 CST 2021
 */

import org.ctfcracktools.fuction.CoreFunc;
import org.ctfcracktools.fuction.PythonFunc;
import org.ctfcracktools.json.PluginsJson;

import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Map;
import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

/**
 * @author 0chencc
 */
public class DecodePanel extends JPanel {
    public DecodePanel() {
        initComponents();
    }
    public void inputCharacterChange(DocumentEvent e){
        input = inputArea.getText();
        int length = inputArea.getText().replace("\r|\n","").length();
        inputCharacterCount.setText("InputArea - Now Input Character Count:"+length);
    }
    public void resultCharacterChange(DocumentEvent e){
        input = inputArea.getText();
        int length = resultArea.getText().replace("\r|\n","").length();
        resultCharacterCount.setText("ResultArea - Now Result Character Count:"+length);
    }
    private void pluginsComboBoxActionPerformed(ActionEvent e) {
        // TODO add your code here
        if (pluginsComboBox.getSelectedIndex()==0){
            return;
        }
        String select = pluginsComboBox.getItemAt(pluginsComboBox.getSelectedIndex());
        PythonFunc pyFunc = new PythonFunc();
        Map<String,Object> plugin = json.search(select);
        String[] prams = {};
        ArrayList<String> keys = new ArrayList<>();
        if (plugin.containsKey("key")){
            keys = (ArrayList<String>) plugin.get("key");
            prams = new String[keys.size()+1];
        }
        pyFunc.loadFile(plugin.get("path").toString());
        if (keys.size()>=1){
            prams[0] = inputArea.getText();
            for (int i = 1;i<prams.length;i++){
                prams[i] = JOptionPane.showInputDialog("Please input "+keys.get(i-1));
            }
            resultArea.setText(pyFunc.execFuncOfArr(pyFunc.loadPythonFunc(pyFunc.interpreter,"main"),prams).toString());
        }else {
            resultArea.setText(pyFunc.execFuncOfArr(pyFunc.loadPythonFunc(pyFunc.interpreter,"main"),inputArea.getText()).toString());
        }
        pluginsComboBox.setSelectedIndex(0);
    }
    private void loadPlugin(){
        plugins = json.parseJson();
        String[] name = new String[plugins.size()+1];
        name[0] = "Plugins as";
        for(int i=1;i<=plugins.size();i++){
            name[i] = String.valueOf(plugins.get(i-1).get("name"));
        }
        DefaultComboBoxModel model = new DefaultComboBoxModel<>(name);
        pluginsComboBox.setModel(model);
    }
    private void reloadPluginsActionPerformed(ActionEvent e) {
        // TODO add your code here
        loadPlugin();
    }

    private void encodeComboBoxActionPerformed(ActionEvent e) {
        // TODO add your code here
        if(encodeComboBox.getSelectedIndex()==0){
            return;
        }
        String select = encodeComboBox.getItemAt(encodeComboBox.getSelectedIndex());
        if ("VigenereEnCode".equals(select)){
            String tmp = JOptionPane.showInputDialog("Please input key");
            char[] key = tmp.toCharArray();
            resultArea.setText(func.vigenereEnCode(input.toCharArray(),key));
        }else {
            resultArea.setText(func.callFunc(input,select));
        }
        encodeComboBox.setSelectedIndex(0);
    }

    private void decodeComboBoxActionPerformed(ActionEvent e) {
        // TODO add your code here
        if (decodeComboBox.getSelectedIndex()==0){
            return;
        }
        String select = decodeComboBox.getItemAt(decodeComboBox.getSelectedIndex());
        if ("VigenereDeCode".equals(select)){
            String tmp = JOptionPane.showInputDialog("Please input key");
            char[] key = tmp.toCharArray();
            resultArea.setText(func.vigenereDeCode(input.toCharArray(),key));
        }else{
            resultArea.setText(func.callFunc(input,select));
        }
        decodeComboBox.setSelectedIndex(0);
    }

    private void decryptComboBoxActionPerformed(ActionEvent e) {
        // TODO add your code here
        if (decryptComboBox.getSelectedIndex()==0){
            return;
        }
        String select = decryptComboBox.getItemAt(decryptComboBox.getSelectedIndex());
        resultArea.setText(func.callFunc(input,select));
        decryptComboBox.setSelectedIndex(0);
    }

    private void decodeComboBoxItemStateChanged(ItemEvent e) {
        // TODO add your code here
    }
    private void initComponents() {
        // JFormDesigner - Component initialization - DO NOT MODIFY  //GEN-BEGIN:initComponents
        inputCharacterCount = new JLabel();
        scrollPane1 = new JScrollPane();
        inputArea = new JTextArea();
        encodeComboBox = new JComboBox<>();
        decodeComboBox = new JComboBox<>();
        decryptComboBox = new JComboBox<>();
        pluginsComboBox = new JComboBox<>();
        reloadPlugins = new JButton();
        resultCharacterCount = new JLabel();
        scrollPane2 = new JScrollPane();
        resultArea = new JTextArea();

        //======== this ========
        setLayout(new GridBagLayout());
        ((GridBagLayout)getLayout()).columnWidths = new int[] {0, 0, 0, 0, 0, 0, 0, 0};
        ((GridBagLayout)getLayout()).rowHeights = new int[] {0, 0, 0, 0, 0, 0};
        ((GridBagLayout)getLayout()).columnWeights = new double[] {0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 1.0E-4};
        ((GridBagLayout)getLayout()).rowWeights = new double[] {0.0, 1.0, 0.0, 0.0, 1.0, 1.0E-4};

        //---- inputCharacterCount ----
        inputCharacterCount.setText("InputArea - Now Input Character Count:0");
        add(inputCharacterCount, new GridBagConstraints(0, 0, 7, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //======== scrollPane1 ========
        {

            //---- inputArea ----
            inputArea.setLineWrap(true);
            scrollPane1.setViewportView(inputArea);
        }
        add(scrollPane1, new GridBagConstraints(0, 1, 7, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //---- encodeComboBox ----
        encodeComboBox.setModel(new DefaultComboBoxModel<>(new String[] {
            "Encode as"
        }));
        encodeComboBox.addActionListener(e -> encodeComboBoxActionPerformed(e));
        add(encodeComboBox, new GridBagConstraints(1, 2, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 5), 0, 0));

        //---- decodeComboBox ----
        decodeComboBox.setModel(new DefaultComboBoxModel<>(new String[] {
            "Decode as"
        }));
        decodeComboBox.addActionListener(e -> decodeComboBoxActionPerformed(e));
        add(decodeComboBox, new GridBagConstraints(2, 2, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 5), 0, 0));

        //---- decryptComboBox ----
        decryptComboBox.setModel(new DefaultComboBoxModel<>(new String[] {
            "Decrypt as"
        }));
        decryptComboBox.addActionListener(e -> decryptComboBoxActionPerformed(e));
        add(decryptComboBox, new GridBagConstraints(3, 2, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 5), 0, 0));

        //---- pluginsComboBox ----
        pluginsComboBox.setModel(new DefaultComboBoxModel<>(new String[] {
            "Plugins as"
        }));
        pluginsComboBox.addActionListener(e -> pluginsComboBoxActionPerformed(e));
        add(pluginsComboBox, new GridBagConstraints(4, 2, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 5), 0, 0));

        //---- reloadPlugins ----
        reloadPlugins.setText("Reload Plugins");
        reloadPlugins.addActionListener(e -> reloadPluginsActionPerformed(e));
        add(reloadPlugins, new GridBagConstraints(5, 2, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 5), 0, 0));

        //---- resultCharacterCount ----
        resultCharacterCount.setText("ResultArea - Now Result Character Count:0");
        add(resultCharacterCount, new GridBagConstraints(0, 3, 7, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //======== scrollPane2 ========
        {

            //---- resultArea ----
            resultArea.setLineWrap(true);
            scrollPane2.setViewportView(resultArea);
        }
        add(scrollPane2, new GridBagConstraints(0, 4, 7, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 0, 0), 0, 0));
        // JFormDesigner - End of component initialization  //GEN-END:initComponents
        //输入监听
        inputArea.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void removeUpdate(DocumentEvent e) {
                inputCharacterChange(e);
            }
            @Override
            public void insertUpdate(DocumentEvent e) {
                inputCharacterChange(e);
            }
            @Override
            public void changedUpdate(DocumentEvent e) {
                inputCharacterChange(e);
            }
        });
        //结果输出监听
        resultArea.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void removeUpdate(DocumentEvent e) {
                resultCharacterChange(e);
            }
            @Override
            public void insertUpdate(DocumentEvent e) {
                resultCharacterChange(e);
            }
            @Override
            public void changedUpdate(DocumentEvent e) {
                resultCharacterChange(e);
            }
        });
        DefaultComboBoxModel encodeModel = new DefaultComboBoxModel(new String[]{
                "Encode as",
                "MorseEncode",
                "BaconEncode",
                "Base64Encode",
                "Base32Encode",
                "UrlEncode",
                "UnicodeEncode",
                "HTMLEncode",
                "VigenereEnCode"
        });
        DefaultComboBoxModel decodeModel = new DefaultComboBoxModel(new String[]{
                "Decode as",
                "MorseDecode",
                "BaconDecode",
                "Base64Decode",
                "Base32Decode",
                "UrlDecode",
                "UnicodeDecode",
                "HTMLDecode",
                "VigenereDeCode"
        });
        DefaultComboBoxModel decryptModel = new DefaultComboBoxModel(new String[]{
                "Decrypt as",
                "Fence",
                "CaesarCode",
                "PigCode",
                "Rot13",
                "Hex2String",
                "String2Hex",
                "Unicode2Ascii",
                "Ascii2Unicode",
                "Reverse"
        });
        encodeComboBox.setModel(encodeModel);
        decodeComboBox.setModel(decodeModel);
        decryptComboBox.setModel(decryptModel);
        loadPlugin();
    }

    // JFormDesigner - Variables declaration - DO NOT MODIFY  //GEN-BEGIN:variables
    private JLabel inputCharacterCount;
    private JScrollPane scrollPane1;
    private JTextArea inputArea;
    private JComboBox<String> encodeComboBox;
    private JComboBox<String> decodeComboBox;
    private JComboBox<String> decryptComboBox;
    private JComboBox<String> pluginsComboBox;
    private JButton reloadPlugins;
    private JLabel resultCharacterCount;
    private JScrollPane scrollPane2;
    private JTextArea resultArea;
    // JFormDesigner - End of variables declaration  //GEN-END:variables
    private final CoreFunc func = new CoreFunc();
    private final PluginsJson json = new PluginsJson();
    private ArrayList<Map<String,Object>> plugins = json.parseJson();
    private String input;
}
