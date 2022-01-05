package org.ctfcracktools.ui;/*
 * Created by JFormDesigner on Thu Nov 25 10:28:49 CST 2021
 */

import org.ctfcracktools.fuction.CodeMode;
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
        if (CodeMode.ENCODE_VIGENERE.equals(select)){
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
        if (CodeMode.DECODE_VIGENERE.equals(select)){
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
                CodeMode.ENCODE_MORSE,
                CodeMode.ENCODE_BACON,
                CodeMode.ENCODE_BASE64,
                CodeMode.ENCODE_BASE32,
                CodeMode.ENCODE_URL,
                CodeMode.ENCODE_UNICODE,
                CodeMode.ENCODE_HTML,
                CodeMode.ENCODE_VIGENERE,
        });
        DefaultComboBoxModel decodeModel = new DefaultComboBoxModel(new String[]{
                "Decode as",
                CodeMode.DECODE_MORSE,
                CodeMode.DECODE_BACON,
                CodeMode.DECODE_BASE64,
                CodeMode.DECODE_BASE32,
                CodeMode.DECODE_URL,
                CodeMode.DECODE_UNICODE,
                CodeMode.DECODE_HTML,
                CodeMode.DECODE_VIGENERE,
        });
        DefaultComboBoxModel decryptModel = new DefaultComboBoxModel(new String[]{
                "Decrypt as",
                CodeMode.CRYPTO_FENCE,
                CodeMode.CRYPTO_CAESAR,
                CodeMode.CRYPTO_PIG,
                CodeMode.CRYPTO_ROT13,
                CodeMode.CRYPTO_HEX_2_STRING,
                CodeMode.CRYPTO_STRING_2_HEX,
                CodeMode.CRYPTO_UNICODE_2_ASCII,
                CodeMode.CRYPTO_ASCII_2_UNICODE,
                CodeMode.CRYPTO_REVERSE
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
