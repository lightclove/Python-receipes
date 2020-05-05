package ceeport.tools;

//download snmp4j-2.2.1.jar (or newer) from snmp4j.org (look in maven repository)
//compile with javac -classpath snmp4j-2.2.1.jar:. snmpTrap.java
//java -classpath snmp4j-2.2.1.jar:. snmpTrap
import java.util.Iterator;
import java.util.Vector;

import org.snmp4j.CommandResponder;
import org.snmp4j.CommandResponderEvent;
import org.snmp4j.MessageDispatcherImpl;
import org.snmp4j.MessageException;
import org.snmp4j.PDU;
import org.snmp4j.Snmp;
import org.snmp4j.log.ConsoleLogFactory;
import org.snmp4j.log.LogAdapter;
import org.snmp4j.log.LogFactory;
import org.snmp4j.log.LogLevel;
import org.snmp4j.mp.MPv1;
import org.snmp4j.mp.MPv2c;
import org.snmp4j.mp.MPv3;
import org.snmp4j.mp.StatusInformation;
import org.snmp4j.security.AuthSHA;
import org.snmp4j.security.PrivAES128;
import org.snmp4j.security.SecurityModels;
import org.snmp4j.security.SecurityProtocols;
import org.snmp4j.security.USM;
import org.snmp4j.security.UsmUser;
import org.snmp4j.smi.Address;
import org.snmp4j.smi.OctetString;
import org.snmp4j.smi.UdpAddress;
import org.snmp4j.smi.VariableBinding;
import org.snmp4j.transport.DefaultUdpTransportMapping;
import org.snmp4j.util.MultiThreadedMessageDispatcher;
import org.snmp4j.util.ThreadPool;

//our main class
public class snmpTrap implements CommandResponder {
	// configuration
	private static boolean _logging = false;

	private String _securityname = "security name";

	private String _authphrase = "authentication phrase";

	private String _privacyphrase = "privacy phrase";

	private String _listenaddress = "0.0.0.0/162";// listen on all
													   // interfaces on port
													   // 1620, traditionally
													   // snmp informs sent to
													   // port 162
	// end configuration

	private DefaultUdpTransportMapping transport; // for tcp
	// private DefaultUdpTransportMapping transport; //for udp

	private static LogAdapter logger = null;

	public snmpTrap() {
		try {
			if (_logging) {
				logger.setLogLevel(LogLevel.ALL);
				System.out.println("INFO PRINT Mode is on...");
			}
		} catch (Exception e) {
			// continue without error, debug will be off
		}
	}

	private void initSNMP() throws Exception {

		// The engine id below remains the same across restarts and creates
		// issues when Trap sending applications
		// run for a long period of time and expect the engine id to remain
		// running with a given uptime.
		// When the app is restarted, the uptime resets, and the client receives
		// an error that is encapsulated
		// in an OID: usmStatsNotInTimeWindows; OID, 1.3.6.1.6.3.15.1.1.2
		// The below code makes sure that the engine id is never the same (based
		// on epoch time), and this solves that problem.

		// OctetString localEngineID = new
		// OctetString(MPv3.createLocalEngineID());
		String epoch = String.valueOf(System.currentTimeMillis() / 1000);
		OctetString localEngineID = new OctetString("ABC" + epoch);
		ThreadPool threadPool = ThreadPool.create("Trap", 5);// start 5 threads
															 // to handle 5
															 // connections
															 // simultaneously
		MultiThreadedMessageDispatcher dispatcher = new MultiThreadedMessageDispatcher(
				threadPool, new MessageDispatcherImpl());
		// tcp
//		Address listenAddress = GenericAddress.parse(System.getProperty(
//				"snmp4j.listenAddress", _listenaddress));

		Address targetAddress = new UdpAddress(_listenaddress);
		transport = new DefaultUdpTransportMapping((UdpAddress) targetAddress);
		
		// udp
		// Address listenAddressu =
		// GenericAddress.parse(System.getProperty("snmp4j.listenAddress",
		// "udp:0.0.0.0/1062"));
		// DefaultUdpTransportMapping transport = new
		// DefaultUdpTransportMapping((UdpAddress)listenAddressu);
		SecurityProtocols.getInstance().addDefaultProtocols();
		SecurityProtocols.getInstance()
				.addAuthenticationProtocol(new AuthSHA());// Use SHA encryption
														  // for authentication
		SecurityProtocols.getInstance().addPrivacyProtocol(new PrivAES128()); // Use
																			  // AES
																			  // 128
																			  // Bit
																			  // encryption
																			  // for
																			  // privacy
																			  // /
																			  // encryption.
																			  // Net-SNMP
																			  // uses
																			  // 128
																			  // Bit
																			  // AES
																			  // encryption
																			  // by
																			  // default,
																			  // 192/256
																			  // bit
																			  // encryption
																			  // won't
																			  // work.
		USM usm = new USM(SecurityProtocols.getInstance(), localEngineID, 0);
		UsmUser usera = new UsmUser(new OctetString(_securityname), // security
																	// name
				AuthSHA.ID, // authprotocol
				new OctetString(_authphrase), // authpassphrase
				PrivAES128.ID, // privacyprotocol
				new OctetString(_privacyphrase) // privacypassphrase
		);
		Snmp snmp = new Snmp(dispatcher, transport);
		snmp.getMessageDispatcher().addMessageProcessingModel(
				new MPv1());
		snmp.getMessageDispatcher().addMessageProcessingModel(
				new MPv2c());
		snmp.getMessageDispatcher().addMessageProcessingModel(
				new MPv3());		
		SecurityModels.getInstance().addSecurityModel(usm);
		snmp.getUSM().addUser(usera);
		snmp.addCommandResponder(this);

		if (logger.isInfoEnabled()) {
			logger.info("Snmp Receiver is now listening for connections");
		}
		snmp.listen();
	}

	public static void main(String[] args) {
		// setup logging factory
		LogFactory.setLogFactory(new ConsoleLogFactory());
		logger = LogFactory.getLogger(snmpTrap.class);
		snmpTrap ts = new snmpTrap();
		try {
			ts.initSNMP();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	// inform packets require a response, this function creates and sends the
	// response (From the SNMP4J Library examples)
	protected void sendInformResponse(CommandResponderEvent event)
			throws MessageException {
		PDU responsePDU = (PDU) event.getPDU().clone();
		responsePDU.setType(PDU.RESPONSE);
		responsePDU.setErrorStatus(PDU.noError);
		responsePDU.setErrorIndex(0);
		event.getMessageDispatcher().returnResponsePdu(
				event.getMessageProcessingModel(), event.getSecurityModel(),
				event.getSecurityName(), event.getSecurityLevel(), responsePDU,
				event.getMaxSizeResponsePDU(), event.getStateReference(),
				new StatusInformation());
	}

	// triggered everytime an SNMP message is successfully received because this
	// class implements CommandResponder
	public void processPdu(CommandResponderEvent e) {
		if (logger.isInfoEnabled()) {
			logger.info("Entering the processing step of the PDU");
		}
		// get the pdu (SNMP message OIDs essentially)
		PDU thetrap = e.getPDU();
		if (logger.isInfoEnabled()) {
			logger.info("Successfully got the PDU");
		}

		if (logger.isInfoEnabled()) {
			logger.info("Processing the varbindings");
		}
		String json_trap = "";

		// iterate through the pdu's contents
		Vector<? extends VariableBinding> v = thetrap.getVariableBindings();
		Iterator<? extends VariableBinding> it = v.iterator();
		for (; it.hasNext();) {

			VariableBinding i = it.next();

			// create the array key using the oid key
			json_trap += "\"" + i.getOid().toString() + "\":\""
					+ i.getVariable().toString() + "\",\n";
		}
		// trim final comma and newline on json_trap
		json_trap = json_trap.substring(0, json_trap.length() - 2);
		// print the trap's contents
		System.out.println("TRAP CONTENTS:\n " + json_trap);
		try {
			sendInformResponse(e);
		} catch (Exception ee) {
			ee.printStackTrace();
		}

		e.setProcessed(true);
		if (logger.isInfoEnabled()) {
			logger.info("Processed the PDU");
		}
	}
	
	
	
//    private void snmpSendV3(String agentAddress, OID oids) {
//        try {
//
//            PDU pdu = new ScopedPDU();
//            pdu.add(new VariableBinding(new OID(SYS_UPTIME_OID)));
//            pdu.setType(PDU.GET);
//            
//            if(snmpTrap == null) {
//                System.out.println("creating  snmp");
//                TransportMapping transport = new DefaultUdpTransportMapping();
//                snmpTrap = new Snmp(transport);
//                transport.listen();
//
//                USM usm = new USM(SecurityProtocols.getInstance(), new OctetString(MPv3.createLocalEngineID()), 0);
//                SecurityModels.getInstance().addSecurityModel(usm);
//
//                snmpTrap.getUSM().addUser(new OctetString(COMMUNITY), new UsmUser(new OctetString(COMMUNITY), null, null, null, null));
//                
//            }
//            
//
//            Address targetAddress = GenericAddress.parse(agentAddress);
//            UserTarget target = new UserTarget();
//            //target.setCommunity(new OctetString("public"));
//            target.setAddress(targetAddress);
//            target.setRetries(1);
//            target.setTimeout(5000);
//            target.setVersion(SnmpConstants.version3);
//            target.setSecurityLevel(SecurityLevel.NOAUTH_NOPRIV);
//            target.setSecurityName(new OctetString(COMMUNITY));
//
//            snmpSend.listen();
//
//            ResponseEvent response = snmpSend.send(pdu, target);
//            if (response.getResponse() != null) {
//                PDU responsePDU = response.getResponse();
//                System.out.println("response = " + responsePDU);
//                if (responsePDU != null) {
//                    if (responsePDU.getErrorStatus() == PDU.noError) {
//                        return;
//                    }
//                }
//            }
//
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//    }
	
	
}
	
/*
 * //upon successful SNMP inform submission, this will output Entering the
 * processing step of the PDU Successfully got the PDU Processing the
 * varbindings TRAP CONTENTS: "1.3.6.1.2.1.1.3.0":"20691031",
 * "1.3.6.1.6.3.1.1.4.1.0":"1.3.6.1.4.1.1236.2.1.5.6.2",
 * "1.3.6.1.2.1.1.5.0":"1", "1.3.6.1.4.1.1236.1.1.1.1.1.0":"999-999-1000",
 * "1.3.6.1.4.1.1236.1.1.1.4.1.0":"1",
 * "1.3.6.1.2.1.1.2.0":"1.3.6.1.4.1.1236.1.1" Processed the PDU NOTIFICATION
 * RECEIVED, A connection from 127.0.0.1/44591 changed state... 2 Closing the
 * connection Socket to 127.0.0.1/44591 closed Socket to 127.0.0.1/44591 closed
 * due to timeout
 */