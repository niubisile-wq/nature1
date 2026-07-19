# Cover letter

Date: 19 July 2026

Dear Editor,

We are pleased to submit our manuscript, "A geospatial signal-processing workflow for auditing observability bias in InSAR-derived subsidence exposure estimates", for consideration as an original research article in *Earth Science Informatics*.

Public InSAR products are increasingly used for subsidence screening and exposure assessment, but downstream workflows often treat missing or weakly observable radar support as if it were decision-neutral. This can change the denominator of exposure accounting and can understate the population or built environment that requires additional monitoring. Our manuscript addresses this informatics problem by separating deformation relevance, radar-product observability and exposure before summarizing risk-facing quantities.

The manuscript contributes a reproducible geospatial signal-processing workflow that converts public InSAR valid support into an observability mask, intersects it with a frozen strong-deformation screen and reports hidden exposure using area-weighted and native-pixel accounting. In the Chao Phraya urban delta lead case, the workflow identifies 3.77 million people and 404.77 km2 of built-up land in not-majority-observable portions of strong-deformation cells; a native GHSL-pixel sensitivity gives 3.63 million people and 404.77 km2. Robustness tests cover threshold surfaces, block-size sensitivity, Monte Carlo propagation and decision-ranking changes.

The evidence strategy is deliberately bounded. The manuscript uses a completed DWR/TRE--GHSL Central Valley positive-control setting, a completed Cyprus EGMS near-zero boundary control and code-path test, a Po River Delta non-EGMS transfer case supported by published sparse GNSS/InSAR context and Japan/Iran product-lineage tests. Prepared Po/Rhone EGMS scripts and query payloads are retained as reproducible future hooks, but the manuscript does not claim a completed Po/Rhone EGMS strong-subsidence benchmark or dense site-level validation of every hidden cell.

We believe the manuscript fits *Earth Science Informatics* because its primary contribution is an information-processing and reproducibility framework for translating public Earth-observation products into exposure estimates while preserving product-support uncertainty. The work is intended for readers using geospatial signal processing, SAR/InSAR products and spatial data fusion for Earth-system risk screening, especially where public products are used before dense local validation is available.

All data and code supporting the manuscript are available through the GitHub and Zenodo links reported in the Data and code availability statement. The manuscript is original, is not under consideration elsewhere and has been approved by all authors. The authors declare no competing interests.

Thank you for considering our submission.

Sincerely,

Zixuan Liu  
Detroit Green Technology Institute, Hubei University of Technology  
Wuhan 430068, China  
Email: 2411621306@hbut.edu.cn
