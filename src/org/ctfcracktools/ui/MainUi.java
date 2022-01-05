package org.ctfcracktools.ui;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

import org.ctfcracktools.ui.*;
import org.jetbrains.annotations.NotNull;
/*
 * Created by JFormDesigner on Wed Nov 24 18:42:26 CST 2021
 */



/**
 * @author 0chencc
 */
public class MainUi extends JPanel {
    public MainUi() {
        initComponents();
    }
    public void closeTabActionPerformed(ActionEvent e){
        if (tabbedPane2.getTabCount()>2){
            if (tabbedPane2.getSelectedIndex()!=0){
                tabbedPane2.remove(tabbedPane2.getSelectedIndex());
                tabbedPane2.setSelectedIndex(tabbedPane2.getSelectedIndex()-1);
            }else{
                tabbedPane2.remove(tabbedPane2.getSelectedIndex());
                tabbedPane2.setSelectedIndex(tabbedPane2.getSelectedIndex());
            }
        }
    }
    private void initComponents() {
        // JFormDesigner - Component initialization - DO NOT MODIFY  //GEN-BEGIN:initComponents
        tabbedPane1 = new JTabbedPane();
        tabbedPane2 = new JTabbedPane();
        decodePanel1 = new DecodePanel();
        decodePanel2 = new DecodePanel();
        autoConvertRadix1 = new AutoConvertRadix();
        pluginsConfig1 = new PluginsConfig();
        settingConfig1 = new SettingConfig();
        about1 = new About();

        //======== this ========
        setLayout(new GridBagLayout());
        ((GridBagLayout)getLayout()).columnWidths = new int[] {0, 0};
        ((GridBagLayout)getLayout()).rowHeights = new int[] {0, 0};
        ((GridBagLayout)getLayout()).columnWeights = new double[] {1.0, 1.0E-4};
        ((GridBagLayout)getLayout()).rowWeights = new double[] {1.0, 1.0E-4};

        //======== tabbedPane1 ========
        {

            //======== tabbedPane2 ========
            {
                tabbedPane2.addTab("1", decodePanel1);
                tabbedPane2.addTab("...", decodePanel2);
            }
            tabbedPane1.addTab("DaE", tabbedPane2);
            tabbedPane1.addTab("RadiexConvert", autoConvertRadix1);
            tabbedPane1.addTab("PluginsConfig", pluginsConfig1);
            tabbedPane1.addTab("SettingConfig", settingConfig1);
            tabbedPane1.addTab("About", about1);
        }
        add(tabbedPane1, new GridBagConstraints(0, 0, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 0, 0), 0, 0));
        // JFormDesigner - End of component initialization  //GEN-END:initComponents
        tabSwitch = new TabTitleEditListener(tabbedPane2);
        tabbedPane2.addChangeListener(tabSwitch);
        tabbedPane2.addMouseListener(tabSwitch);
        closeTab.addActionListener(e -> closeTabActionPerformed(e));
        tabMenu.add(closeTab);
    }

    // JFormDesigner - Variables declaration - DO NOT MODIFY  //GEN-BEGIN:variables
    private JTabbedPane tabbedPane1;
    private JTabbedPane tabbedPane2;
    private DecodePanel decodePanel1;
    private DecodePanel decodePanel2;
    private AutoConvertRadix autoConvertRadix1;
    private PluginsConfig pluginsConfig1;
    private SettingConfig settingConfig1;
    private About about1;
    // JFormDesigner - End of variables declaration  //GEN-END:variables
    protected static JPopupMenu tabMenu = new JPopupMenu();
    private JMenuItem closeTab = new JMenuItem("Delete");
    private TabTitleEditListener tabSwitch;
}
class TabTitleEditListener extends MouseAdapter implements ChangeListener, DocumentListener {
    protected final JTextField editor = new JTextField();
    protected final JTabbedPane tabbedPane;
    protected int editingIdx = -1;
    protected int len = -1;
    protected Boolean listen = true;
    protected Dimension dim;
    protected Component tabComponent;
    protected Boolean isRenameOk = false;
    protected final Action startEditing = new AbstractAction() {
        @Override public void actionPerformed(ActionEvent e) {
            editingIdx = tabbedPane.getSelectedIndex();
            tabComponent = tabbedPane.getTabComponentAt(editingIdx);
            tabbedPane.setTabComponentAt(editingIdx, editor);
            isRenameOk = true;
            editor.setVisible(true);
            editor.setText(tabbedPane.getTitleAt(editingIdx));
            editor.selectAll();
            editor.requestFocusInWindow();
            len = editor.getText().length();
            dim = editor.getPreferredSize();
            editor.setMinimumSize(dim);
        }
    };
    protected final Action renameTabTitle = new AbstractAction() {
        @Override public void actionPerformed(ActionEvent e) {
            String title = editor.getText().trim();
            if (editingIdx >= 0 && !title.isEmpty()) {
                String oldName = tabbedPane.getTitleAt(editingIdx);
                tabbedPane.setTitleAt(editingIdx, title);
            }
            cancelEditing.actionPerformed(null);
        }
    };
    protected final Action cancelEditing = new AbstractAction() {
        @Override public void actionPerformed(ActionEvent e) {
            if (editingIdx >= 0) {
                tabbedPane.setTabComponentAt(editingIdx, tabComponent);
                editor.setVisible(false);
                editingIdx = -1;
                len = -1;
                tabComponent = null;
                editor.setPreferredSize(null);
                tabbedPane.requestFocusInWindow();
            }
        }
    };

    protected TabTitleEditListener(JTabbedPane tabbedPane) {
        super();
        this.tabbedPane = tabbedPane;
        editor.setBorder(BorderFactory.createEmptyBorder());
        editor.addFocusListener(new FocusAdapter() {
            @Override public void focusLost(FocusEvent e) {
                renameTabTitle.actionPerformed(null);
            }
        });
        InputMap im = editor.getInputMap(JComponent.WHEN_FOCUSED);
        ActionMap am = editor.getActionMap();
        im.put(KeyStroke.getKeyStroke(KeyEvent.VK_ESCAPE, 0), "cancel-editing");
        am.put("cancel-editing", cancelEditing);
        im.put(KeyStroke.getKeyStroke(KeyEvent.VK_ENTER, 0), "rename-tab-title");
        am.put("rename-tab-title", renameTabTitle);
        editor.getDocument().addDocumentListener(this);
        tabbedPane.getInputMap(JComponent.WHEN_FOCUSED).put(KeyStroke.getKeyStroke(KeyEvent.VK_ENTER, 0), "start-editing");
        tabbedPane.getActionMap().put("start-editing", startEditing);
    }
    @Override public void stateChanged(ChangeEvent e) {
        if (e.getSource() instanceof JTabbedPane && listen) {
            JTabbedPane pane = (JTabbedPane) e.getSource();
            if (!isRenameOk){
                if (pane.getSelectedIndex() == pane.getComponentCount()-1){
                    newTab();
                }
            }else{
                if (pane.getSelectedIndex() == pane.getComponentCount()-2){
                    newTab();
                }
            }
        }
        renameTabTitle.actionPerformed(null);
    }
    public void newTab(){
        insertTab(tabbedPane);
    }
    public void insertTab(JTabbedPane pane){
        pane.addTab(String.valueOf(pane.getTabCount()),new DecodePanel());
        pane.remove(pane.getSelectedIndex());
        pane.addTab("...",new JLabel());
    }
    public void setListen(Boolean listen){
        this.listen = listen;
    }
    @Override public void insertUpdate(DocumentEvent e) {
        updateTabSize();
    }

    @Override public void removeUpdate(DocumentEvent e) {
        updateTabSize();
    }

    @Override public void changedUpdate(DocumentEvent e) {}

    @Override public void mouseClicked(MouseEvent e) {
        switch (e.getButton()){
            case 1:
            {
                Rectangle r = tabbedPane.getBoundsAt(tabbedPane.getSelectedIndex());
                boolean isDoubleClick = e.getClickCount() >= 2;
                if (isDoubleClick && r.contains(e.getPoint())) {
                    startEditing.actionPerformed(null);
                } else {
                    renameTabTitle.actionPerformed(null);
                }
                break;
            }
            case 3:{
                MainUi.tabMenu.show(e.getComponent(),e.getX(),e.getY());
                break;
            }
            default:
                break;
        }
    }

    protected void updateTabSize() {
        editor.setPreferredSize(editor.getText().length() > len ? null : dim);
        tabbedPane.revalidate();
    }
}