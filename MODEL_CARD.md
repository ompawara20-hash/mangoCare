# Model Card: MangoCare AI Vision Models

## 1. Primary Disease Classification Model

### 1.1 Model Details
- **Model Name:** Mango Disease ConvNeXt Classifier (`ixrbhii/mango-disease-convnext`)
- **Architecture:** ConvNeXt-Small (`convnext_small.fb_in22k_ft_in1k`)
- **Total Parameters:** 49,460,840 (~49.5 Million)
- **Model Format:** SafeTensors (`model.safetensors`, 98.9 MB) & PyTorch `timm` integration
- **Source / Repository:** [Hugging Face Hub: ixrbhii/mango-disease-convnext](https://huggingface.co/ixrbhii/mango-disease-convnext)
- **Publisher / Maintainer:** Community open-source research contributor `ixrbhii` (hosted on Hugging Face Hub)
- **License:** Apache License 2.0 (Permits commercial and non-commercial redistribution and modification)
- **Date Information Checked:** October 2026

### 1.2 Dataset Provenance
- **Dataset Name:** MangoLeafBD / Mango Leaf Disease Benchmark Dataset
- **Domain:** Field-collected mango foliar specimens under natural daylight and orchard conditions
- **Classes Count:** 8 distinct phytopathological and entomological conditions
- **Foliar vs Fruit Distinction:** **IMPORTANT NOTICE:** This model is trained specifically on **mango leaves and foliage**, NOT harvested fruit surfaces. Mango foliar symptoms (such as foliar anthracnose lesions, powdery mildew dusting on young flushes, and bacterial canker water-soaked spots) indicate orchard pathogen presence, but visual leaf inference must not be treated as a definitive harvested fruit postharvest disorder classification.

### 1.3 Supported Classes
1. `Anthracnose` (*Colletotrichum gloeosporioides*)
2. `Bacterial Canker` (*Xanthomonas citri pv. mangiferaeindicae*)
3. `Cutting Weevil` (*Deporaus marginatus*)
4. `Die Back` (*Lasiodiplodia theobromae*)
5. `Gall Midge` (*Procontarinia matteiana*)
6. `Healthy` (*Normal healthy leaf tissue*)
7. `Powdery Mildew` (*Oidium mangiferae*)
8. `Sooty Mould` (*Meliola mangiferae / Capnodium mangiferae*)

### 1.4 Input Specifications & Preprocessing
- **Color Mode:** RGB (3 channels)
- **Resolution:** $224 \times 224$ pixels
- **Interpolation:** Bilinear
- **EXIF Handling:** Automatic transposition using Pillow orientation tags
- **Normalization:**
  - Mean: $[0.485, 0.456, 0.406]$
  - Standard Deviation: $[0.229, 0.224, 0.225]$
- **Crop Mode:** Center crop with scale preservation

### 1.5 Inference Procedure & Output Format
- **Forward Pass:** PyTorch in `eval()` mode under `torch.no_grad()` or `torch.inference_mode()`.
- **Output:** Logits vector of dimension $[1, 8]$ converted to probabilities via softmax:
  $$\sigma(z)_i = \frac{e^{z_i}}{\sum_{j=1}^8 e^{z_j}}$$
- **Confidence Scoring & Uncertainty:**
  - High confidence ($\ge 0.70$): Candidate class identified.
  - Moderate confidence ($0.50 \le p < 0.70$): Suggestive visual indication.
  - Low confidence ($< 0.50$): Categorized as **Inconclusive / Uncertain**; prompts the user to provide a sharper, closer photograph under diffused natural lighting.

### 1.6 Evaluation Metrics
- **Validation Accuracy reported by dataset benchmarks:** Evaluated against the standard test split of the MangoLeafBD benchmark with over 96% top-1 accuracy on held-out leaf test partitions.
- **Real-World Domain Shift Caution:** Published benchmark accuracy on curated dataset splits does not guarantee identical performance across distinct orchard microclimates, varying cultivars (e.g., Alphonso vs Tommy Atkins vs Dasheri), extreme shadow/glare, or novel biotypes.

---

## 2. Mango Image Validation Model (Non-Mango Rejection)

### 2.1 Model Details
- **Model Name:** MobileNetV3-Small Object & Scene Screener
- **Architecture:** `mobilenet_v3_small` (PyTorch official torchvision weights: `MobileNet_V3_Small_Weights.DEFAULT`)
- **Total Parameters:** 2,542,856 (~2.5 Million, 9.8 MB)
- **Publisher:** PyTorch / Torchvision team (ImageNet-1K pretrained)
- **Role:** Screen uploads before disease classification to reject clearly unrelated objects (vehicles, humans, domestic animals, furniture, text documents, electronics) and confirm agricultural/botanical context.

### 2.2 Validation Pipeline Strategy
1. **File & Image Integrity Checks:** Validates decoding, checks image dimensions ($100 \times 100$ minimum, $6000 \times 6000$ maximum), rejects non-image or corrupted uploads.
2. **Color & Foliage Spectral Check:** Analyzes RGB channel distribution to verify presence of chlorophyll/organic plant hues and rejects artificial blank pages, screenshots, or documents.
3. **Pretrained Screener:** Flags high-confidence non-botanical classes (e.g., cars, dogs, people, buildings, electronic devices).
4. **Result:** If an image fails validation, the system immediately returns a structured `MANGO_NOT_DETECTED` error code, aborting disease inference cleanly without producing fabricated diagnostic claims.

---

## 3. Ethical Use & Diagnostic Disclaimer
MangoCare AI is strictly designed as an **educational and preliminary agricultural screening instrument**. Visual image analysis cannot detect internal latent fungal mycelia, vascular wilts inside heavy trunks, or soil-borne root rots. It must never substitute for laboratory plant pathology (microscopy, PCR, bacterial culturing) or certified on-site agronomist inspections.
