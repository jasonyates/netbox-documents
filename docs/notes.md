# Notes Feature in NetBox v3.6+

NetBox v3.6 introduces a new **Notes** feature, allowing users to attach informal, free-text annotations to various objects (e.g., devices, IP addresses, circuits).

---

## ✨ Overview

The Notes feature is ideal for adding ad-hoc observations, operational reminders, or collaboration-oriented comments to existing objects in the system.

## 🧭 How to Use

1. Go to the detail page of an object (like a Device or Prefix).
2. Scroll down to the **Notes** panel.
3. Click **"Add Note"**.
4. Type your message and click **Save**.

## 🔒 Permissions

- All users with **view permission** for the parent object can see its notes.
- Only the **note creator** or users with explicit **edit/delete permissions** on `Note` objects can modify or delete them.

## 💡 Use Cases

- Track quick updates or maintenance logs
- Share decisions with teammates without cluttering formal fields
- Document troubleshooting steps for future reference

---

This lightweight feature increases collaboration and improves object traceability while keeping structured data clean.
