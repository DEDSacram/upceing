# Lab 04 — BPMN Order Process (Camunda)

Model an order process in BPMN 2.0 XML and run it on Camunda via Docker.

## 1. Theory

- **BPMN 2.0** = standard business-process notation: start/end events, tasks (service/user), exclusive gateways (XOR), sequence flows. The `.bpmn` file is executable XML.
- **Camunda** = workflow engine executing BPMN. You deploy the XML to the engine; service tasks call workers/connectors; user tasks appear in Tasklist.
- **This process:** `order received → check stock (XOR) → [in stock: charge payment → ship] / [out of stock: notify customer] → end`. Payment uses a service task (external worker topic `charge-payment`); notification is a user task for the demo.
- **Tokens:** one token per instance flows along sequence flows; XOR gateway routes on `${inStock}` variable.

## 2. Project layout

```
lab-04-bpmn-camunda/
  README.md
  order-process.bpmn    # deployable BPMN 2.0 (Camunda 7 compatible, no vendor extensions required)
  docker-compose.yml    # Camunda 7 + Postgres note
```

## 3. Run

```bash
cd labs/NAPIS/lab-04-bpmn-camunda
# validate XML well-formedness (no engine needed)
python3 -c "import xml.etree.ElementTree as ET; ET.parse('order-process.bpmn'); print('BPMN XML OK')"

# full engine run (needs Docker)
docker compose up -d
# open http://localhost:8080/camunda (demo/demo), deploy order-process.bpmn,
# start instance with variable inStock=true, complete user tasks in Tasklist.
docker compose down
```

## 4. Verify

1. XML parses and contains one `process`, one `startEvent`, ≥1 `exclusiveGateway`, ≥2 `endEvent`.
2. After deploy, Cockpit shows the process definition `order-process`.
3. Two instances (`inStock=true/false`) take the two different gateway branches.

## 5. Tasks

1. Add a timer boundary event on the shipment task (e.g. 2 days → escalate).
2. Replace the `notify customer` user task with a mail send-task (connector) and document variables.
3. Add a compensation path for failed payment (gateway + `refund` task).
4. Export a historic instance diagram from Cockpit and note token paths.
