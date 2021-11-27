package org.ctfcracktools.ui;/*
 * Created by JFormDesigner on Thu Nov 25 11:35:29 CST 2021
 */

import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Vector;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.DefaultTableModel;

import org.ctfcracktools.fuction.PythonFunc;
import org.ctfcracktools.json.PluginsJson;
import org.ctfcracktools.json.SettingJson;

/**
 * @author 0chencc
 */
public class PluginsConfig extends JPanel {
    public PluginsConfig() {
        initComponents();
    }

    private void removePluginActionPerformed(ActionEvent e) {
        // TODO add your code here
        PluginsJson json = new PluginsJson();
        String t = pluginsList.getSelectedValue().toString();
        Map<String,Object> plugin = json.search(t);
        json.removePlugin(plugin);
        name.remove(t);
        pluginsList.setListData(name);
    }

    private void addPluginActionPerformed(ActionEvent e) {
        // TODO add your code here
        PluginsJson json = new PluginsJson();
        ArrayList<Map<String,Object>> plugins = json.parseJson();
        JFileChooser selectFile = new JFileChooser();
        selectFile.setFileSelectionMode(JFileChooser.FILES_ONLY);
        FileNameExtensionFilter filter = new FileNameExtensionFilter("Plugin File (.py)","py");
        selectFile.setFileFilter(filter);
        int selectFrame = selectFile.showDialog(new JLabel(),"Select");
        if (selectFrame == JFileChooser.APPROVE_OPTION){
            String pluginPath = selectFile.getSelectedFile().toString();
            PythonFunc pyFunc = new PythonFunc();
            Map<String,Object> plugin = pyFunc.getAuthorInfo(pluginPath);
            plugin.put("path",pluginPath);
            plugins.add(plugin);
            json.writeJson(plugins);
            name.add(plugin.get("name").toString());
            pluginsList.setListData(name);
        }
    }

    private void pluginsListMouseClicked(MouseEvent e) {
        // TODO add your code here
        DefaultTableModel model = new DefaultTableModel();
        PluginsJson json = new PluginsJson();
        Map<String,Object> plugin = json.search(pluginsList.getSelectedValue().toString());
        detailTable.setModel(model);
        Vector<Vector<Object>> detail = new Vector<>();
        for(Map.Entry<String,Object> i :plugin.entrySet()){
            Vector<Object> item = new Vector<>();
            item.add(i.getKey());
            item.add(i.getValue());
            detail.add(item);
        }
        Vector<String> title = new Vector<>();
        title.add("Item");
        title.add("Detail");
        model.setDataVector(detail,title);
    }

    private void initComponents() {
        // JFormDesigner - Component initialization - DO NOT MODIFY  //GEN-BEGIN:initComponents
        label1 = new JLabel();
        addPlugin = new JButton();
        scrollPane3 = new JScrollPane();
        pluginsList = new JList();
        removePlugin = new JButton();
        label2 = new JLabel();
        scrollPane1 = new JScrollPane();
        detailTable = new JTable();

        //======== this ========
        setLayout(new GridBagLayout());
        ((GridBagLayout)getLayout()).columnWidths = new int[] {55, 0, 0};
        ((GridBagLayout)getLayout()).rowHeights = new int[] {0, 36, 0, 49, 0, 32, 0};
        ((GridBagLayout)getLayout()).columnWeights = new double[] {0.0, 1.0, 1.0E-4};
        ((GridBagLayout)getLayout()).rowWeights = new double[] {0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0E-4};

        //---- label1 ----
        label1.setText("Plugins");
        add(label1, new GridBagConstraints(0, 0, 2, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //---- addPlugin ----
        addPlugin.setText("add");
        addPlugin.addActionListener(e -> addPluginActionPerformed(e));
        add(addPlugin, new GridBagConstraints(0, 1, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 5), 0, 0));

        //======== scrollPane3 ========
        {

            //---- pluginsList ----
            pluginsList.addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    pluginsListMouseClicked(e);
                }
            });
            scrollPane3.setViewportView(pluginsList);
        }
        add(scrollPane3, new GridBagConstraints(1, 1, 1, 3, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //---- removePlugin ----
        removePlugin.setText("remove");
        removePlugin.addActionListener(e -> removePluginActionPerformed(e));
        add(removePlugin, new GridBagConstraints(0, 2, 1, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 5), 0, 0));

        //---- label2 ----
        label2.setText("Plugin Detail");
        add(label2, new GridBagConstraints(0, 4, 2, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 5, 0), 0, 0));

        //======== scrollPane1 ========
        {

            //---- detailTable ----
            detailTable.setModel(new DefaultTableModel(
                new Object[][] {
                    {null, null},
                    {null, null},
                },
                new String[] {
                    "Item", "Detail"
                }
            ));
            scrollPane1.setViewportView(detailTable);
        }
        add(scrollPane1, new GridBagConstraints(0, 5, 2, 1, 0.0, 0.0,
            GridBagConstraints.CENTER, GridBagConstraints.BOTH,
            new Insets(0, 0, 0, 0), 0, 0));
        // JFormDesigner - End of component initialization  //GEN-END:initComponents
        PluginsJson json = new PluginsJson();
        ArrayList<Map<String, Object>> plugins = json.parseJson();
        name = new Vector<>();
        for(Map<String,Object> i:plugins){
            name.add(i.get("name").toString());
        }
        pluginsList.setListData(name);
    }

    // JFormDesigner - Variables declaration - DO NOT MODIFY  //GEN-BEGIN:variables
    private JLabel label1;
    private JButton addPlugin;
    private JScrollPane scrollPane3;
    private JList pluginsList;
    private JButton removePlugin;
    private JLabel label2;
    private JScrollPane scrollPane1;
    private JTable detailTable;
    // JFormDesigner - End of variables declaration  //GEN-END:variables
    private Vector<String> name;
};

