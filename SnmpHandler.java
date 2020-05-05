package ceeport.netManage.snmp;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import ceeport.netManage.device.IDevice;
import ceeport.netManage.device.impl.AccessPoint;
import ceeport.netManage.device.impl.AccessPointController;
import ceeport.netManage.device.impl.CentralSwitch;
import ceeport.netManage.device.impl.SubSwitch;
import ceeport.netManage.device.impl.phone.Phone;
import ceeport.netManage.device.impl.phone.PhoneClient;
import ceeport.netManage.device.state.DeviceState;
import ceeport.netManage.gui.MainData;
import ceeport.netManage.util.BsoriLogger;
import ceeport.tools.Pinger;
import org.snmp4j.CommunityTarget;
import org.snmp4j.PDU;
import org.snmp4j.Snmp;
import org.snmp4j.TransportMapping;
import org.snmp4j.event.ResponseEvent;
import org.snmp4j.mp.MPv3;
import org.snmp4j.mp.SnmpConstants;
import org.snmp4j.security.SecurityModels;
import org.snmp4j.security.SecurityProtocols;
import org.snmp4j.security.USM;
import org.snmp4j.security.UsmUser;
import org.snmp4j.smi.GenericAddress;
import org.snmp4j.smi.OID;
import org.snmp4j.smi.OctetString;
import org.snmp4j.smi.VariableBinding;
import org.snmp4j.transport.DefaultUdpTransportMapping;

/**
 * This class sends PDU requests to SNMP agents (polling)
 */
public class SnmpHandler {

    final static BsoriLogger LOGGER = BsoriLogger.getLogger(SnmpHandler.class);

    //public static Logger logger = Logger.getLogger(SnmpHandler.class.getName());
    private static final String COMMUNITY = "ISGKP";
    private static final OID SYS_NAME_OID = new OID(".1.3.6.1.2.1.1.5.0");
    private static final OID wcAccessPointIp = new OID(".1.3.6.1.4.1.4526.100.8.2.3.1.1.2");
    private static final OID wcAccessPointName = new OID(".1.3.6.1.4.1.4526.100.8.2.4.1.1.4");
    private static final OID wcClientApIp = new OID(".1.3.6.1.4.1.4526.100.8.2.4.1.1.5");
    private static final OID wcClientApName = new OID(".1.3.6.1.4.1.4526.100.8.2.4.1.1.4");
    private static ArrayList<String> wcAccessPointIpList = new ArrayList<String>();

    private static final OID wcAccessPointState = new OID(".1.3.6.1.4.1.4526.100.8.2.3.1.1.17.0");
    private static ArrayList<String> wcAccessPointStateList = new ArrayList<String>();

    private static OID wcClientMac = new OID("1.3.6.1.4.1.4526.100.8.2.4.1.1.1");
    //private static String[] wcClientMacList = {"90:f6:52:12:ed:ff", "4c:21:d0:82:2e:43", "1c:7b:21:2f:c4:a3", "1c:7b:21:30:4b:ce", "1c:7b:21:22:7f:5a", "1c:7b:21:30:4b:61", "1c:7b:21:86:41:7d", "1c:7b:21:30:79:16", "1c:7b:21:22:84:bd", "4c:21:d0:82:2e:85", "1c:7b:21:22:84:48", "1c:7b:21:84:b7:e1", "1c:7b:21:86:42:77", "4c:21:d0:82:1f:2a", "18:00:2d:09:7a:ac", "1c:7b:21:30:7e:28", "1c:7b:21:86:41:72", "1c:7b:21:30:7e:74", "1c:7b:21:22:86:4e", "1c:7b:21:86:43:58", "1c:7b:21:86:43:7f"};

    private static OID wcClientIp = new OID("1.3.6.1.4.1.4526.100.8.2.4.1.1.2");

    private static SnmpHandler instance;
    private MainData mainData;
    private Snmp snmpTrap;
    private Snmp snmpSend;


    // thread pool for submitting polling tasks
    ThreadPoolExecutor executor = new ThreadPoolExecutor(
            500, // corePoolSize
            700, // maxPoolSize
            5000, // keepAliveTime
            TimeUnit.MILLISECONDS,
            new LinkedBlockingQueue<Runnable>(500)); // max tasks in the queue

    public static synchronized SnmpHandler getInstance() {
        if (instance == null) {
            instance = new SnmpHandler();
        }
        return instance;
    }

    public synchronized void start() {
        try {
            createSnmpSend();
            //listen(new UdpAddress("0.0.0.0/162"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Since snmp4j relies on asynch req/resp we need a listener
    // for responses which should be closed
    public void stop() throws IOException, InterruptedException {
        snmpTrap.close();


    }

    /**
     * Trap Listener
     */
//    private synchronized void listen(TransportIpAddress address) throws IOException {
//        AbstractTransportMapping transport;
//        if (address instanceof TcpAddress) {
//            transport = new DefaultTcpTransportMapping((TcpAddress) address);
//        } else {
//            transport = new DefaultUdpTransportMapping((UdpAddress) address);
//        }
//        ThreadPool threadPool = ThreadPool.create("TrapPool", 30);// start 5 threads
//        // to handle 5
//        MultiThreadedMessageDispatcher dispatcher = new MultiThreadedMessageDispatcher(
//                threadPool, new MessageDispatcherImpl());
//        SecurityProtocols.getInstance().addDefaultProtocols();
//        USM usm = new USM(SecurityProtocols.getInstance(), new OctetString(MPv3.createLocalEngineID()), 0);
//        UsmUser usera = new UsmUser(new OctetString(COMMUNITY), // security
//                null,
//                null,
//                null,
//                null
//        );
//        snmpTrap = new Snmp(dispatcher, transport);
//        snmpTrap.getMessageDispatcher().addMessageProcessingModel(
//                new MPv1());
//        snmpTrap.getMessageDispatcher().addMessageProcessingModel(
//                new MPv2c());
//        snmpTrap.getMessageDispatcher().addMessageProcessingModel(
//                new MPv3());
//        SecurityModels.getInstance().addSecurityModel(usm);
//        snmpTrap.getUSM().addUser(new OctetString(COMMUNITY), usera);
//        snmpTrap.addCommandResponder(new CommandResponder() {
//            @Override
//            public void processPdu(CommandResponderEvent cre) {
//                throw new UnsupportedOperationException("Not supported yet.");
//            }
//        });
//
//        //////////////////////////////////////////////
//        transport.listen();
//        //System.out.println( "Listening on " + address);
//        System.out.println("Listening on " + address);
//
////		try {
////			this.wait();
////		} catch (InterruptedException ex) {
////			Thread.currentThread().interrupt();
////		}
//    }
    private void createSnmpSend() throws IOException {
        //System.out.println( "creating  snmp sender");
        System.out.println("creating  snmp sender");
        TransportMapping transport = new DefaultUdpTransportMapping();
        snmpSend = new Snmp(transport);
        transport.listen();
        USM usm = new USM(SecurityProtocols.getInstance(), new OctetString(MPv3.createLocalEngineID()), 0);
        SecurityModels.getInstance().addSecurityModel(usm);
        snmpSend.getUSM().addUser(new OctetString(COMMUNITY), new UsmUser(new OctetString(COMMUNITY), null, null, null, null));
    }

    public void pollSwitches(final IDevice device) throws Throwable {

        // For the date & time output in the response
        final long curTime = System.currentTimeMillis();
        final Date curDate = new Date(curTime);
        final String curStringDate = new SimpleDateFormat("dd.MM.yyyy").format(curTime);
        //-------------------------------------------------------------------------------
        if (!(device instanceof SubSwitch) && !(device instanceof CentralSwitch)) {
            return;
        }
        if(device instanceof CentralSwitch  && device.getState() == DeviceState.OFF) device.disableIncludingAllChildren();
        //if(device instanceof SubSwitch  && device.getState() == DeviceState.OFF) device.disableIncludingAllChildren();
        String deviceIp = device.getIpAddress();
        if (deviceIp == null) {
            return;
        }

        try {
            String s = getStringSnmpResponse(deviceIp, 161, COMMUNITY, SYS_NAME_OID);
            if (s != null) {
                device.setState(DeviceState.ON);
                System.out.println("Получен ответ от устройства с именем: \"" + device.getName() + "\" и ip адресом: " + device.getIpAddress());

            } else {
//                device.setState(DeviceState.BROKEN);
//                System.out.println("Broken connection or empty or wrong snmp response data!");
//                TimeUnit.SECONDS.sleep(2);
                device.setState(DeviceState.OFF);
                System.out.println("Не получен ответ от устройства с именем: \"" + device.getName() + "\" и ip адресом: " + device.getIpAddress());
            }

        } catch (IOException | NullPointerException e) {
            System.out.println("catched!");
            device.setState(DeviceState.BROKEN);
        }

    }

    public void pollAllDevices() throws Throwable {
        if (mainData == null || mainData.getAllDevices() == null) {
            return;
        }

        for (final IDevice device : mainData.getAllDevices()) {
            executor.execute(new Runnable() {
                @Override
                public void run() {
                    try {
                        pollAPsClients(device);
                        pollSwitches(device);
                        pollAccessPointController(device);

                    } catch (Throwable ex) {
                        System.out.println(ex);
                        ex.printStackTrace();
                    }
                }
            });
        }
    }

    /**
     * @return the mainData
     */
    public MainData getMainData() {
        return mainData;
    }

    /**
     * @param mainData the mainData to set
     */
    public void setMainData(MainData mainData) {
        this.mainData = mainData;
    }

    public ArrayList<String> getTabularSnmpResponse(String address, int port, String community, OID oid, int maxRepetitions) throws Throwable {

        CommunityTarget target = new CommunityTarget();
        target.setAddress(GenericAddress.parse("udp:" + address + "/" + port));
        target.setCommunity(new OctetString(community));
        target.setRetries(5);
        target.setTimeout(5000);
        target.setVersion(SnmpConstants.version2c);
        PDU pdu = new PDU();
        pdu.add(new VariableBinding(oid));
        pdu.setType(PDU.GETBULK);
        pdu.setMaxRepetitions(maxRepetitions);
        pdu.setNonRepeaters(0);
        ResponseEvent responseEvent = snmpSend.send(pdu, target);
        PDU response = responseEvent.getResponse();

        ArrayList<String> tmpResponseList = new ArrayList<String>();
        try {
            for (int i = 0; i < response.size(); i++) {
                VariableBinding variableBinding = response.get(i);
                tmpResponseList.add(variableBinding.toString().substring(variableBinding.toString().indexOf('='), variableBinding.toString().length()).substring(2));
                //System.out.println(variableBinding.toString().substring(variableBinding.toString().indexOf('='), variableBinding.toString().length()).substring(2));
                //System.out.println("------------------------------------------------------------------------------------------------------------------------------");
            }
        } catch (Throwable e) {
            //System.out.println("SNMP service is not responded from  " + address);
            System.out.println("Cannot get response from " + address + " because of snmp manager's result calculation..." );
            //e.printStackTrace();
        }
//        }catch (NullPointerException n) {
//            //System.out.println("Cannot get response from " + address);
//            System.out.println("Cannot get response from " + address);
//            n.printStackTrace();
//        }

        return tmpResponseList;

    }

    public String getStringSnmpResponse(String address, int port, String community, OID oid) throws Throwable {

        CommunityTarget target = new CommunityTarget();
        target.setAddress(GenericAddress.parse("udp:" + address + "/" + port));
        target.setCommunity(new OctetString(community));
        target.setRetries(3);
        target.setTimeout(100);
        target.setVersion(SnmpConstants.version2c);
        PDU pdu = new PDU();
        pdu.add(new VariableBinding(oid));
        pdu.setType(PDU.GET);
        pdu.setNonRepeaters(0);
        ResponseEvent responseEvent = snmpSend.send(pdu, target);
        PDU response = responseEvent.getResponse();

        String sResponce = null;
        if (response != null) {
            sResponce = response.toString().substring(response.toString().lastIndexOf(61) + 2, response.toString().length() - 2);
            //System.out.println(sResponce);
        } else {
            System.out.println("No response for OID: " + oid);
        }
        return sResponce;
    }

    public void pollAccessPointController(IDevice device) throws Throwable {

        String parseAccessPointControllerSysName = getStringSnmpResponse("10.168.2.50", 161, COMMUNITY, SYS_NAME_OID);

        if (device instanceof AccessPointController) {
            try {
                if (!parseAccessPointControllerSysName.equals(null) || !parseAccessPointControllerSysName.equals("")) {
                    device.setState(DeviceState.ON);
                } else {
                    device.setState(DeviceState.OFF); // end inner if
                }
            } catch (Exception e) {
                device.setState(DeviceState.BROKEN);
                e.printStackTrace();
            }
            //pingDevices(device);
        }// end outer if

        if (!(device instanceof AccessPoint)) {
            return;
        } //end if

        String deviceIp = device.getIpAddress();
        if (deviceIp == null) {
            return;
        } //end if

        ArrayList<String> parseAccessPointIp = getTabularSnmpResponse("10.168.2.50", 161, COMMUNITY, wcAccessPointIp, 40);
        ArrayList<String> parsePointState = getTabularSnmpResponse("10.168.2.50", 161, COMMUNITY, wcAccessPointState, 40);

        for (int i = 0; i < parseAccessPointIp.size(); i++) {
            if (device.getIpAddress().equals(parseAccessPointIp.get(i))) {

                try {
                    if (parsePointState.get(i).equals("Connected")) {
                        device.setState(DeviceState.ON);
                        System.out.println("device " + device.getIpAddress() + " " + device.getName() + " with ip: \"" + device.getIpAddress()+ "\" is ON");
                    } else {
                        device.setState(DeviceState.OFF);
                        System.out.println("device " + device.getIpAddress() + " " + device.getName() + " with ip: \"" + device.getIpAddress()+ "\" is NOT responded ");
                    } //end inner if

                } catch (IndexOutOfBoundsException iobe) {
                    System.out.println("Asynchronious snmp response data - list are data different in size");
                    //device.setState(DeviceState.BROKEN);
                    System.out.println("device is not responded " + device.getIpAddress());
                    iobe.printStackTrace();
                }

            } //end outer if
        } //end for

    }

    public void pollAPsClients(IDevice device) throws Throwable {

        if (!(device instanceof AccessPoint)) {
            return;
        }

//        if(device instanceof CentralSwitch)
//            if(device.getState() == DeviceState.OFF)

        // show all APs with connected clients
        ArrayList<String> parseAPnames = getTabularSnmpResponse("10.168.2.50", 161, COMMUNITY, wcClientApName, 40);

        // show all connected clients' macs
        ArrayList<String> parseClientMacs = getTabularSnmpResponse("10.168.2.50", 161, COMMUNITY, wcClientMac, 40);

        // show all connected clients' ips
        ArrayList<String> parseClientIps = getTabularSnmpResponse("10.168.2.50", 161, COMMUNITY, wcClientIp, 40);

        // Set of unique MACs, used toх filter out garbage (clients with duplicating macs)
        Set<String> macsSet = new HashSet<String>();

        Collection<PhoneClient> phoneClients = new ArrayList<>();

        for (int i = 0; i < parseAPnames.size(); i++) {
            //System.out.println(i + " " + parseAPnames.get(i) + " = " + parseClientMacs.get(i));
            try {
                String mac = parseClientMacs.get(i);

                if (!mac.toUpperCase().matches("^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$")) {
                    break;
                }

                if (parseAPnames.get(i).equals(device.getName())) {

                    if (macsSet.contains(mac)) {
                        continue; // skip duplicate macs
                    }
                    macsSet.add(mac);

                    PhoneClient phoneClient = new PhoneClient();
                    //phoneClient.setName("");
                    //phoneClient.setId(i + 1);
                    //phoneClient.setIp(ip);
                    phoneClient.setMac(mac);
                    phoneClients.add(phoneClient);
                }
            }//end of try
            catch (IndexOutOfBoundsException ii) {
                System.out.println(ii);
            }//end of catch
        }

        AccessPoint accessPoint = (AccessPoint) device;
        Phone phone = accessPoint.getPhone();
        phone.setPhoneClients(phoneClients);
        phone.render();
    }

    //    private static Collection<PhoneClient> testClients;
//
//    static {
//    	testClients = generateRandomPhoneClients();
//    }
//
//	private static Collection<PhoneClient> generateRandomPhoneClients() {
//		if(testClients != null) {
//			return testClients;
//		}
//		testClients = new ArrayList<PhoneClient>();
//
//		Random r = new Random();
//		int numberOfClients = r.nextInt(40);
//		String macAddr = "AA:BB:CC:DD:";
//		for(int i = 0; i < numberOfClients; i++) {
//			PhoneClient phoneClient = new PhoneClient();
//			phoneClient.setName(UUID.randomUUID().toString().replaceAll("-", ""));
//			phoneClient.setId(i + 1);
//			phoneClient.setIp(r.nextInt(256) + "." + r.nextInt(256) + "." + r.nextInt(256) + "." + r.nextInt(256));
//			phoneClient.setMac(String.format(macAddr + "%02X:%02X", i, i));
//			testClients.add(phoneClient);
//		}
//		return testClients;
//	}


}

