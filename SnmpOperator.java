package ceeport.tools;

import java.io.IOException;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Vector;
import org.snmp4j.CommunityTarget;
import org.snmp4j.PDU;
import org.snmp4j.Snmp;
import org.snmp4j.Target;
import org.snmp4j.event.ResponseEvent;
import org.snmp4j.mp.SnmpConstants;
import org.snmp4j.smi.Address;
import org.snmp4j.smi.OID;
import org.snmp4j.smi.OctetString;
import org.snmp4j.smi.TcpAddress;
import org.snmp4j.smi.UdpAddress;
import org.snmp4j.smi.VariableBinding;
import org.snmp4j.transport.AbstractTransportMapping;
import org.snmp4j.transport.DefaultTcpTransportMapping;
import org.snmp4j.transport.DefaultUdpTransportMapping;
import org.snmp4j.util.DefaultPDUFactory;
import org.snmp4j.util.TreeEvent;
import org.snmp4j.util.TreeListener;
import org.snmp4j.util.TreeUtils;

public class SnmpOperator {

    private String host;
    private String transport = "udp";
    private int port = 161;
    private int version = SnmpConstants.version2c;
    private OctetString community = new OctetString("ISGKP");
    private int retrys = 3;
    private int timeout = 1000;
    private int pduType = PDU.GETNEXT;
    private int maxRepetitions = 10;
    private int nonRepeaters = 0;
    private int maxSizeResponsePDU = 65535;
    private Vector vbs = new Vector();

    private Snmp snmp = null;
    private PDU request = null;
    private Target target = null;
    private long times;

    public SnmpOperator() {
        super();
    }

    public SnmpOperator(String host, int port, int version, OctetString community) {
        super();
        this.host = host;
        this.port = port;
        this.version = version;
        this.community = community;
    }

    public SnmpOperator(String host, int port, int version, OctetString community, int pduType) {
        super();
        this.host = host;
        this.port = port;
        this.version = version;
        this.community = community;
        this.pduType = pduType;
    }

    private Snmp createSnmpSession() throws IOException {
        AbstractTransportMapping transport;
        if (getAddress(host) instanceof TcpAddress) {
            transport = new DefaultTcpTransportMapping();
        } else {
            transport = new DefaultUdpTransportMapping();
        }
        Snmp snmp = new Snmp(transport);
        return snmp;
    }

    private Target createTarget() {
        CommunityTarget target = new CommunityTarget();
        target.setCommunity(community);
        return target;
    }

    public PDU createPDU(Target target) {
        PDU request = new PDU();
        request.setType(pduType);
        return request;
    }

    private Address getAddress(String transportAddress) {
        if (transportAddress.indexOf('/') < 0) {
            transportAddress += "/" + port;
        }
        if (transport.equalsIgnoreCase("udp")) {
            return new UdpAddress(transportAddress);
        } else if (transport.equalsIgnoreCase("tcp")) {
            return new TcpAddress(transportAddress);
        }
        throw new IllegalArgumentException("Unknown transport " + transport);
    }

    private boolean init() {
        try {
            snmp = createSnmpSession();
            target = createTarget();
            target.setVersion(version);
            target.setAddress(getAddress(host));
            target.setRetries(retrys);
            target.setTimeout(timeout);
            target.setMaxSizeRequestPDU(maxSizeResponsePDU);
            snmp.listen();

            request = createPDU(target);
            if (request.getType() == PDU.GETBULK) {
                request.setMaxRepetitions(maxRepetitions);
                request.setNonRepeaters(nonRepeaters);
            }
            for (int i = 0; i < vbs.size(); i++) {
                request.add((VariableBinding) vbs.get(i));
                //System.out.println("vbs is "+vbs.get(i)+"  "+vbs.size());
            }
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public HashMap get() throws IOException {
        PDU response;
        HashMap hm = null;
        init();
        ResponseEvent responseEvent;
        long startTime = System.currentTimeMillis();
        responseEvent = null;
        responseEvent = snmp.send(request, target);

        if (responseEvent != null) {
            response = null;
            response = responseEvent.getResponse();
            if (response != null) {
                if (response.getVariableBindings().size() > 0) {
                    hm = new HashMap();
                }
				//for (int j = 0;j < this.request.getVariableBindings().size();j++) {
                //System.out.println("request oid is "+this.request.getVariableBindings().get(j).toString());
                //}
                //System.out.println(response.toString());
                for (int i = 0; i < response.getVariableBindings().size(); i++) {
                    String pause = response.getVariableBindings().get(i).toString();
                    String getvalue = pause.substring(pause.indexOf(" = ") + 2);
                    String oid = pause.substring(0, pause.indexOf(" ="));
                    //System.out.println("oid is "+oid+"   getvalue is "+getvalue);
                    hm.put(oid.trim(), getvalue.trim());
                }
            } else {
                System.out.println(new Date() + "  response is null.");
            }
            times = System.currentTimeMillis() - startTime;
        }
        snmp.close();
        return hm;
    }

    public List gets() throws IOException {
        init();
        return null;
    }

    public HashMap walk() throws IOException {
        init();
        HashMap snapshot = new HashMap();
        walk(snmp, request, target, snapshot);
        return snapshot;
    }

    private void walk(Snmp snmp, PDU request, Target target, final Map snapshot)
            throws IOException {
        request.setNonRepeaters(0);

        final WalkCounts counts = new WalkCounts();
        final long startTime = System.currentTimeMillis();
        TreeUtils treeUtils = new TreeUtils(snmp, new DefaultPDUFactory());
        TreeListener treeListener = new TreeListener() {
            public boolean next(TreeEvent e) {
                counts.requests++;
                if (e.getVariableBindings() != null) {
                    VariableBinding[] vbs = e.getVariableBindings();
                    counts.objects += vbs.length;
                    for (int i = 0; i < vbs.length; i++) {
                        if (snapshot != null) {
                            String getvalue = vbs[i].getVariable().toString();
                            String oid = vbs[i].getOid().toString();
                            //System.out.println("oid is "+oid+"   getvalue is "+getvalue);
                            snapshot.put(oid.trim(), getvalue.trim());
                        }
                    }
                }
                return true;
            }

            public void finished(TreeEvent e) {
                if ((e.getVariableBindings() != null)
                        && (e.getVariableBindings().length > 0)) {
                    next(e);
                }
                times = System.currentTimeMillis() - startTime;
                if (e.isError()) {
                    System.err.println("The following error occurred during walk:");
                    System.err.println(e.getErrorMessage());
                }
                synchronized (this) {
                    this.notify();
                }
            }

            @Override
            public boolean isFinished() {
                throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
            }
        };
        synchronized (treeListener) {
            OID rootOID = null;
            for (int i = 0; i < request.size(); i++) {
                rootOID = request.get(i).getOid();
                //System.out.println(rootOID);
                treeUtils.getSubtree(target, rootOID, null, treeListener);
                try {
                    treeListener.wait();
                    //System.out.println("unlock : "+rootOID);
                } catch (InterruptedException ex) {
                    System.err.println("Tree retrieval interrupted: "
                            + ex.getMessage());
                    Thread.currentThread().interrupt();
                }
            }
        }
    }

    public OctetString getCommunity() {
        return community;
    }

    public void setCommunity(String community) {
        this.community = new OctetString(community);
    }

    public void setCommunity(OctetString community) {
        this.community = community;
    }

    public String getHost() {
        return host.toString();
    }

    public void setHost(String host) {
        this.host = host;
    }

    public int getMaxRepetitions() {
        return maxRepetitions;
    }

    public void setMaxRepetitions(int maxRepetitions) {
        this.maxRepetitions = maxRepetitions;
    }

    public int getMaxSizeResponsePDU() {
        return maxSizeResponsePDU;
    }

    public void setMaxSizeResponsePDU(int maxSizeResponsePDU) {
        this.maxSizeResponsePDU = maxSizeResponsePDU;
    }

    public int getNonRepeaters() {
        return nonRepeaters;
    }

    public void setNonRepeaters(int nonRepeaters) {
        this.nonRepeaters = nonRepeaters;
    }

    public int getPduType() {
        return pduType;
    }

    public void setPduType(int pduType) {
        this.pduType = pduType;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public int getRetrys() {
        return retrys;
    }

    public void setRetrys(int retrys) {
        this.retrys = retrys;
    }

    public int getTimeout() {
        return timeout;
    }

    public void setTimeout(int timeout) {
        this.timeout = timeout;
    }

    public int getVersion() {
        return version;
    }

    public void setVersion(int version) {
        this.version = version;
    }

    public String getTransport() {
        return transport;
    }

    public void setTransport(String transport) {
        this.transport = transport;
    }

    public Vector getVbs() {
        return vbs;
    }

    public void setVbs(Vector vbs) {
        for (int i = 0; i < vbs.size(); i++) {
            this.vbs.add(new VariableBinding(new OID((String) vbs.get(i))));

        }
    }

    public void addOID(String value) {
        vbs.add(new VariableBinding(new OID(value)));
    }

    public long getTimes() {
        return times;
    }

    public HashMap getValue(deviceinfo object, Vector oids, int op) {
        SnmpOperator so = new SnmpOperator();
        so.setHost(object.getIp());
        so.setCommunity(object.getRcommunity());
        so.setVersion(object.getVersion());
        so.setPduType(op);
        so.setVbs(oids);
        try {
            if (op == PDU.GET) {
                return so.get();
            } else {
                return so.walk();
            }
        } catch (IOException e) {
            return null;
        }
    }
}

class WalkCounts {

    public int requests;
    public int objects;
}

class deviceinfo {

    String ip;
    String rcommunity;
    String wcommunity;
    String descri;
    int id = -1;
    ;
	int version;
    int port;
    int dtype = 1;//0:host 1:switcher
    String product_desc;
    String device_id;
    String sysUptime;
    String product_id;
    String name;
    String location;
    String sysService;

    public deviceinfo() {
        this.rcommunity = "ISGKP";
        this.version = 0;
        this.port = 161;
        this.dtype = 1;

    }

    public deviceinfo(String ip, String community, int version, int port, int dtype) {
        this.ip = ip;
        this.rcommunity = community;
        this.version = version;
        this.port = port;
        this.dtype = dtype;
    }

    public String getRcommunity() {
        return rcommunity;
    }

    public void setRcommunity(String community) {
        this.rcommunity = community;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public int getVersion() {
        return version;
    }

    public void setVersion(int version) {
        this.version = version;
    }

    public String getDescri() {
        return descri;
    }

    public void setDescri(String descri) {
        this.descri = descri;
    }

    public int getDtype() {
        return dtype;
    }

    public void setDtype(int dtype) {
        this.dtype = dtype;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getWcommunity() {
        return wcommunity;
    }

    public void setWcommunity(String wcommunity) {
        this.wcommunity = wcommunity;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getDevice_id() {
        return device_id;
    }

    public void setDevice_id(String device_id) {
        this.device_id = device_id;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getProduct_desc() {
        return product_desc;
    }

    public void setProduct_desc(String product_desc) {
        this.product_desc = product_desc;
    }

    public String getProduct_id() {
        return product_id;
    }

    public void setProduct_id(String product_id) {
        this.product_id = product_id;
    }

    public String getSysService() {
        return sysService;
    }

    public void setSysService(String sysService) {
        this.sysService = sysService;
    }

    public String getSysUptime() {
        return sysUptime;
    }

    public void setSysUptime(String sysUptime) {
        this.sysUptime = sysUptime;
    }

    public static void main(String[] args) throws IOException {
        //SnmpOperator so = new SnmpOperator("10.168.2.50", 161, 2, new OctetString("ISGKP"));
        //so.addOID(".1.3.6.1.4.1.4526.100.8.2.3.1.1.2.0");
        //so.addOID(".1.3.6.1.2.1.1.5.0");
        //so.walk();
                
    }
}
