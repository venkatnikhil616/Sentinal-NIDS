from scapy.all import sniff, IP, TCP, UDP
from app.services.detection_service import DetectionService
from app.services.logging_service import log_event

detector = DetectionService()


def process_packet(packet):
    try:
        if IP in packet:
            data = {
                "duration": 0,
                "protocol_type": "tcp" if TCP in packet else "udp",
                "service": "http",
                "flag": "SF",
                "src_bytes": len(packet),
                "dst_bytes": len(packet)
            }

            result = detector.detect(data)

            log_event(
                attack_type=result.get("prediction", "unknown"),
                confidence=result.get("confidence", 0),
                severity="high" if result.get("prediction") != "normal" else "low"
            )

            print("Detected:", result)

    except Exception as e:
        print("Error:", e)


def start_sniffing():
    print("🚀 Sniffing started...")
    sniff(prn=process_packet, store=False)
