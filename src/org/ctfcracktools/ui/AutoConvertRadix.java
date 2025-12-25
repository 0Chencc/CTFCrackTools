/*
 * Created by JFormDesigner on Thu Nov 25 16:47:22 CST 2021
 */

package org.ctfcracktools.ui;

import java.awt.*;
import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.math.BigInteger;
import java.util.HashMap;
import java.util.Map;

/**
 * @author 0chencc
 */
public class AutoConvertRadix extends JPanel {
    public AutoConvertRadix() {
        initComponents();
    }
    public void characterChange(DocumentEvent e){
        int selectRadix = inputRadix.getSelectedIndex();
        Map<Integer, Integer> radix = new HashMap(){{
            put(0,2);
            put(1,8);
            put(2,10);
            put(3,16);
        }};
        try {
            BigInteger input = new BigInteger(inputTextField.getText(), radix.get(selectRadix));
            Convert(input);
        }catch (NumberFormatException e1){}
    }
    public void Convert(BigInteger input){
        binaryTextField.setText(input.toString(2));
        octTextField.setText(input.toString(8));
        decTextField.setText(input.toString(10));
        hexTextField.setText(input.toString(16));
        try{
            int diy = Integer.parseInt(diyRadix.getText());
            diyRadixOutput.setText(input.toString(diy));
        }catch (Exception e){}
    }
    private void initComponents() {
        // JFormDesigner - Component initialization - DO NOT MODIFY  //GEN-BEGIN:initComponents
        inputRadix = new JComboBox<>();
        inputTextField = new JTextField();
        label1 = new JLabel();
        binaryTextField = new JTextField();
        label2 = new JLabel();
        octTextField = new JTextField();
        label3 = new JLabel();
        decTextField = new JTextField();
        label4 = new JLabel();
        hexTextField = new JTextField();
        label5 = new JLabel();
        diyRadix = new JTextField();
        diyRadixOutput = new JTextField();

        //======== this ========
        setLayout(new GridBagLayout());
        ((GridBagLayout)getLayout()).columnWidths = new int[] {80, 0, 0};
        ((GridBagLayout)getLayout()).rowHeights = new int[] {0, 0, 0, 0, 0, 0, 0, 0};
        ((GridBagLayout)getLayout()).columnWeights = new double[] {0.0, 1.0, 1.0E-4};
        ((GridBagLayout)getLayout()).rowWeights = new double[] {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0E-4};

        //---- inputRadix ----
        inputRadix.setModel(new DefaultComboBoxModel<>(new String[] {
            "Binary",
            "Octal",
            "Decimal",
            "Hex"
        }));
        add(inputRadix, new GridBagConstraints(0, 0, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(10, 0, 5, 5), 0, 0));
        add(inputTextField, new GridBagConstraints(1, 0, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(10, 0, 5, 0), 0, 0));

        //---- label1 ----
        label1.setText("Binary:");
        add(label1, new GridBagConstraints(0, 1, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 5, 5, 5), 0, 0));
        add(binaryTextField, new GridBagConstraints(1, 1, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //---- label2 ----
        label2.setText("Octal:");
        add(label2, new GridBagConstraints(0, 2, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 5, 5, 5), 0, 0));
        add(octTextField, new GridBagConstraints(1, 2, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //---- label3 ----
        label3.setText("Decimal:");
        add(label3, new GridBagConstraints(0, 3, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 5, 5, 5), 0, 0));
        add(decTextField, new GridBagConstraints(1, 3, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //---- label4 ----
        label4.setText("Hexadecimal:");
        add(label4, new GridBagConstraints(0, 4, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 5, 5, 5), 0, 0));
        add(hexTextField, new GridBagConstraints(1, 4, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //---- label5 ----
        label5.setText("Input the radix you want to convert");
        add(label5, new GridBagConstraints(0, 5, 2, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));
        add(diyRadix, new GridBagConstraints(0, 6, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 0, 5), 0, 0));
        add(diyRadixOutput, new GridBagConstraints(1, 6, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 0, 0), 0, 0));
        // JFormDesigner - End of component initialization  //GEN-END:initComponents
        DocumentListener allTextFieldListener = new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) {characterChange(e);}
            @Override
            public void removeUpdate(DocumentEvent e) {characterChange(e);}
            @Override
            public void changedUpdate(DocumentEvent e) {characterChange(e);}
        };
        inputTextField.getDocument().addDocumentListener(allTextFieldListener);
    }

    // JFormDesigner - Variables declaration - DO NOT MODIFY  //GEN-BEGIN:variables
    private JComboBox<String> inputRadix;
    private JTextField inputTextField;
    private JLabel label1;
    private JTextField binaryTextField;
    private JLabel label2;
    private JTextField octTextField;
    private JLabel label3;
    private JTextField decTextField;
    private JLabel label4;
    private JTextField hexTextField;
    private JLabel label5;
    private JTextField diyRadix;
    private JTextField diyRadixOutput;
    // JFormDesigner - End of variables declaration  //GEN-END:variables
}
