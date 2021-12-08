package org.ctfcracktools;

import java.awt.*;

import com.formdev.flatlaf.FlatLightLaf;
import org.ctfcracktools.ui.*;
import javax.swing.*;
import static javax.swing.WindowConstants.EXIT_ON_CLOSE;

/**
 * @author 0chencc
 */
public class Main {
    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel( new FlatLightLaf() );
        } catch( Exception ex ) {
            System.err.println( "Failed to initialize LaF" );
        }
        String title = "CTFCrackTools %s %s";
        String version = "4.0.2";
        String slogan = "";
        JFrame f = new JFrame(String.format(title, version,slogan));
        Dimension d = Toolkit.getDefaultToolkit().getScreenSize();
        f.setBounds((int)(d.getWidth()-900)/2,(int)d.getWidth()/2-600,900,600);
        MainUi m = new MainUi();
        f.add(m);
        f.setDefaultCloseOperation(EXIT_ON_CLOSE);
        f.setVisible(true);
    }
}