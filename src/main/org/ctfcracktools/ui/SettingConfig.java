/*
 * Created by JFormDesigner on Thu Nov 25 23:55:20 CST 2021
 */

package org.ctfcracktools.ui;

import java.awt.*;
import java.awt.event.*;
import java.util.Map;
import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;

import org.ctfcracktools.json.SettingJson;

/**
 * @author 0chencc
 */
public class SettingConfig extends JPanel {
    public SettingConfig() {
        initComponents();
    }

    private void jythonPathConfirmActionPerformed(ActionEvent e) {
        // TODO add your code here
        SettingJson json = new SettingJson();
        Map<String,String> setting = json.parseJson();
        JFileChooser selectFile = new JFileChooser();
        selectFile.setFileSelectionMode(JFileChooser.FILES_ONLY);
        FileNameExtensionFilter filter = new FileNameExtensionFilter("Jython Jar File (.jar)","jar");
        selectFile.setFileFilter(filter);
        int selectFrame = selectFile.showDialog(new JLabel(),"Select");
        if (selectFrame == JFileChooser.APPROVE_OPTION){
            String jythonPath = selectFile.getSelectedFile().toString();
            setting.put("jython",jythonPath);
            json.writeJson(setting);
            jythonPathTextField.setText(jythonPath);
        }
    }

    private void initComponents() {
        // JFormDesigner - Component initialization - DO NOT MODIFY  //GEN-BEGIN:initComponents
        label1 = new JLabel();
        jythonPathTextField = new JTextField();
        jythonPathConfirm = new JButton();

        //======== this ========
        setLayout(new GridBagLayout());
        ((GridBagLayout)getLayout()).columnWidths = new int[] {0, 0, 0, 0};
        ((GridBagLayout)getLayout()).rowHeights = new int[] {0, 0, 0, 0};
        ((GridBagLayout)getLayout()).columnWeights = new double[] {0.0, 1.0, 0.0, 1.0E-4};
        ((GridBagLayout)getLayout()).rowWeights = new double[] {0.0, 0.0, 0.0, 1.0E-4};

        //---- label1 ----
        label1.setText("Jython-Standalone.jar Path:");
        add(label1, new GridBagConstraints(0, 0, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 5), 0, 0));
        add(jythonPathTextField, new GridBagConstraints(1, 0, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 5), 0, 0));

        //---- jythonPathConfirm ----
        jythonPathConfirm.setText("Select");
        jythonPathConfirm.addActionListener(e -> jythonPathConfirmActionPerformed(e));
        add(jythonPathConfirm, new GridBagConstraints(2, 0, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));
        // JFormDesigner - End of component initialization  //GEN-END:initComponents
        SettingJson json = new SettingJson();
        jythonPathTextField.setText(json.parseJson().get("Jython"));
    }

    // JFormDesigner - Variables declaration - DO NOT MODIFY  //GEN-BEGIN:variables
    private JLabel label1;
    private JTextField jythonPathTextField;
    private JButton jythonPathConfirm;
    // JFormDesigner - End of variables declaration  //GEN-END:variables
}
