Read in [EN][README_GR]
# Environment-ALL

Είμαστε οι EnvironmentAll, μαθητές στο 1ο Γυμνάσιο Αγίου Δημητρίου, Χριστίνα, Βασίλης, Ηλίας, Νικόλας και η καθηγήτριά μας Κατερίνα Asimakopoulou.  

# Η πρότασή μας 

Αφού robot σημαίνει εργασία, αναρωτηθήκαμε αν υπάρχει ρομπότ που να επεξεργάζεται τα αποτελέσματα της Κλιματικής Κρίσης και να τα παρουσιάζει σε μία απλούστερη, συμπυκνωμένη μορφή μέσω γραφημάτων με αποτέλεσμα την χρήση τους στην βελτίωση της γεωργικής παραγωγής/συγκομιδής ή και αύξησης πρασίνου σε μία περιοχή, αστική και μη. Μετά από μία σειρά συνεδριάσεων μεταξύ των μελών της ομάδας μας, καταλήξαμε στις γενικές λειτουργίες του ρομπότ μας. Εν αρχή χρησιμοποιούμε ήδη υπάρχοντα προγράμματα ανοιχτού κώδικα και ορισμένα δημιουργημένα από εμάς.

Το RoboΚλίμUs είναι ικανό να παίρνει μετρήσεις μέσω ειδικών αισθητήρων που διαθέτει 
  - Για την ατμόσφαιρα:
    - Θερμοκρασίας, , 
    - Υγρασίας
    - Ποσότητας διοξειδίου του άνθρακα
  - For soil:
    - pH
    - Θερμοκρασίας

 Μετά από κάθε μέτρηση,τα δεδομένα αποστέλνονται μέσω Bluetooth σε ένα απομακρυσμένο υπολογιστή – κέντρο ελέγχου. Ο υπολογιστής κατέχει μία μεγάλη βάση δεδομένων με στοιχεία από επίσημες πηγές. Τα δεδομένα επεξεργάζονται από μία εφαρμογή γραμμένη σε Python 3 και με την βοήθεια του XlsxWriter δημιουργεί φύλλα του Excel με γραφήματα:

Παρακάτω είναι εικόνες της συνδεσμολογίας:

<img src="/Images/Project_anim.jpg" alt="Animated" width="600"/>
<img src="/Images/Project_schem.jpg" alt="Schematic" width="600"/>

# Κώδικας

Για αυτό το project χρησιμοποιούμε Python 3, μπορείτε να κατεβάσετε την τελευτάια έκδοση [εδώ][pyDownload]. Σιγουρευτείτε ότι έχετε πατήσει το "add Python to PATH" κουμπί κατά την εγκατάσταση

Αφού έχετε κατεβάσει και εγκαταστήσει την Python είναι ώρα να κατεβάσουμε την απαραίτητε βιβλιοθήκες. Πλοηγηθείτε στον φάκελο EnvironmentAll, πατήστε την μπάρα διεύθυνσης και σβήστε τα πάντα, τώρα γράψτε "cmd". Ένα νέο παράθυρο θα ανοίξει.

Σε αυτό το παράθυρο γράψτε:
```
pip install -r requirements.txt
```

Αυτό πρέπει να εγγαταστήσει αυτόματα όλες τις απαραίτητες βιβλιοθήκες.

Τώρα απλά τρέξτε το [Data_Com.py][Data_Com_File]

Για επιπλέον πληροφορίες στο πως να χρησιμοποιείτε το πρόγραμα επισκευφθείτε την [Bonus Υποπαράγραφο](#Bonus)

# Bonus

### Links
- [Demo Βίντεο (Περιγραφή, Ιστορία, η Ομάδα μας και Άλλα)]
- [3D Robot Preview 1.1 (Νεότερη έκδοση)][3DprevLatest]
- [3D Robot Preview (Παλαιότερες εκδόσεις)][3DprevOlder]
- [Tutorial - Λήψη και επεξεργασία δεδομένων Arduino][setupTutorial]
- [Timelapse Κατασκευή του Ρομπότ][Timelapse]

### Επικοινωνία

  | Όνομα | Θέση στην ομάδα | Email |
  | ---- | ------------- | ----- |
  | Ασιμακοπούλου Αικατερίνη | Αρχηγός | kasimako@dad.gr |
  | Ηλιόπουλος Νικόλαος | Μέλος | nilioprobots@gmail.com |
  | Καλιακμάνης Ηλίας | Μέλος | hliaskalliakmanis@gmail.com |
  | Κεραμάρης Βασίλειος | Μέλος | gym.1973.2017@gmail.com |
  | Τουρνάρη Χριστίνα | Μέλος | xristinatournari@gmail.com |

[3DprevLatest]: <https://www.youtube.com/watch?v=U1EAlejeVzY>
[3DprevOlder]: <https://www.youtube.com/playlist?list=PL0-nYuvdRR38VOx6JxywApDNGzup6OFcI>
[pyDownload]: <https://www.python.org/downloads>
[Data_Com_File]: <https://github.com/nickiliopoulosedu/EnvironmentAll/blob/master/Data_Com.py>
[README_GR]: <https://github.com/nickiliopoulosedu/EnvironmentAll/blob/master/README.md>
[setupTutorial]: <https://www.youtube.com/watch?v=-dadtUuFnBA>
[Demo]: <https://www.youtube.com/watch?v=5_BvdWMwudM>
[Timelapse]: <https://youtu.be/5FTF4BOpBkA>
