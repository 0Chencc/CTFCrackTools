/*
 * Created by JFormDesigner on Thu Nov 25 23:37:10 CST 2021
 */

package org.ctfcracktools.ui;

import java.awt.*;
import javax.swing.*;

/**
 * @author 0chencc
 */
public class About extends JPanel {
    public About() {
        initComponents();
    }

    private void initComponents() {
        // JFormDesigner - Component initialization - DO NOT MODIFY  //GEN-BEGIN:initComponents
        scrollPane1 = new JScrollPane();
        textArea1 = new JTextArea();

        //======== this ========
        setLayout(new GridBagLayout());
        ((GridBagLayout)getLayout()).columnWidths = new int[] {0, 0};
        ((GridBagLayout)getLayout()).rowHeights = new int[] {0, 0};
        ((GridBagLayout)getLayout()).columnWeights = new double[] {1.0, 1.0E-4};
        ((GridBagLayout)getLayout()).rowWeights = new double[] {1.0, 1.0E-4};

        //======== scrollPane1 ========
        {

            //---- textArea1 ----
            textArea1.setLineWrap(true);
            scrollPane1.setViewportView(textArea1);
        }
        add(scrollPane1, new GridBagConstraints(0, 0, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 0, 0), 0, 0));
        // JFormDesigner - End of component initialization  //GEN-END:initComponents
        textArea1.setText(about);
    }

    // JFormDesigner - Variables declaration - DO NOT MODIFY  //GEN-BEGIN:variables
    private JScrollPane scrollPane1;
    private JTextArea textArea1;
    // JFormDesigner - End of variables declaration  //GEN-END:variables
    private String about = "Author:0chen(@0chencc)\n" +
            "Twitter:@0chencc\n" +
            "GitHub:https://github.com/0Chencc\n" +
            "Wechat Official Accounts(公众号):XizhouPoetry\n" +
            "Repository Url：https://github.com/0Chencc/CTFCrackTools\n" +
            "米斯特安全团队招CTF选手，有意向联系admin@hi-ourlife.com";
}
