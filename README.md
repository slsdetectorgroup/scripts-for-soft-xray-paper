This repository contains some basic scripts relevant to the paper:
"Single-photon counting pixel detector for soft X-rays"
F. Baruffaldi, A, Bergamaschi, et al.

for questions contact: anna.bergamaschi@psi.ch

Content:
    Scripts:
        file_read.py
            - function to open an EIGER raw open_one_dataset

        fit_scurve.py
            - example of a function to fit a threshold scan with an s-curve

        open_one_dataset.py
            -  this simple script opens one threshold scan dataset,
            plots one full frame, plots the threshold scan of one pixel,
            performs the fit with the scurve function

        calculate_charge_collection_efficiency.py
            - this script calculates the charge collection efficiency 
            as a function of the photon impinging point in a pixel,
            given the charge-cloud dimensions (sigma of a 2d simmetric gaussian)
            and pixel-pitch
            - the output is saved as .txt file in the folder "charge_collection"

        calculate_lgads_spectrum.py
            - this script calculates the simulated spectrum of a single LGADs pixel,
            given the photon energy, charge collection efficiency (see previous script),
            design parameters of the LGAD sensor, electronic noise of the read-out 

    Folders:
        charge_collection
            - the outputs of the script "calculate_charge_collection_efficiency.py" are saved here 

        simulated_absorption
            - .txt files containing simulated photon absorption in silicon,
            produced with Geant4, for different photon energies