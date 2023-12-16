// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;
import "_DataProduct.sol";

contract DataTradingSmartContract {
    address public dataSeller;
    address public dataBuyer;
    uint256 public dataProductPrice;
    uint256 public dataDeposit;
    string public dataIPFSCID;
    bool public isDataCorrect;
    bool public isDataReceived;
    bool public isDataPaid;
    uint256 public similarityScore;
    address public dataProductAddress;

    modifier onlyDataBuyer() {
        require(
            msg.sender == dataBuyer,
            "Only DataBuyer can call this function"
        );
        _;
    }
    // Define the constructor to set the initial state
    constructor(
        address _dataProductAddress,
        address _dataSeller,
        address _dataBuyer
    ) {
        dataSeller = _dataSeller;
        dataBuyer = _dataBuyer;
        dataProductPrice = 0;
        dataDeposit = 0;
        dataIPFSCID = "0x0";
        isDataCorrect = false;
        isDataReceived = false;
        isDataPaid = false;
        similarityScore = 1;
        dataProductAddress = _dataProductAddress;
        
    }
    //notify upload of the score
    event UploadScore(uint256 similarityScore);
    // Function for DataBuyer to initiate the data purchase
    // return the dataCID dataType and dataDescription for evaluation
    function initiateDataPurchase(string memory ipfsCID, address _dataBuyer)
        public
        returns (
            string memory,
            string memory,
            string memory
        )
    {
        // Retrieve data product details from DataProduct contract
        (
            address dataProductOwner,
            string memory dataType,
            string memory dataDescription,
            string memory _ipfsCID,
            string memory sampleData,
            uint256 productPrice
        ) = DataProduct(dataProductAddress).getProductDetails(ipfsCID);
        // Set parameters in DataTradingSmartContract
        dataBuyer = _dataBuyer;
        dataIPFSCID = _ipfsCID;
        dataProductPrice = productPrice;
        dataDeposit = productPrice;
        return (dataType, dataDescription, _ipfsCID);
        // Assuming deposit is the same as product price
    }
    // Function for DataBuyer to pay for the data product and deposit
    function payForDataProduct() public payable onlyDataBuyer {
        // DataBuyer can pay for the product only if called by DataBuyer
        require(
            msg.value == dataProductPrice + dataDeposit,
            "Payment amount must match the product price and deposit"
        );
        isDataPaid = true;
    }
    //data buyer use the key to decode the dataset and confirm data received
    // ignore the dataset encode key send cycle
    function confirmDataReceived(bool _isDataReveived) public onlyDataBuyer {
        require(
            isDataPaid,
            "DataBuyer must have paid for the product and deposit."
        );
        isDataReceived = _isDataReveived;
    }
    // Function for DataBuyer to confirm data receipt and check data
    function confirmDataReceipt(bool _isDataCorrect) public payable onlyDataBuyer {
        // DataBuyer can confirm data receipt only if called by DataBuyer
        require(isDataPaid, "DataBuyer must have paid.");
        require(isDataReceived, "DataBuyer must have received.");

        isDataCorrect = _isDataCorrect;

        if (isDataCorrect) {
            payable(dataSeller).transfer(dataProductPrice);
            DataProduct(dataProductAddress).returnDeposit(dataIPFSCID);
            withdrawDeposit();
            // Data is correct, no additional action needed
        } else {
            // data buyer think the data is not correct, so the data will be evaluated with ai;
            evaluateData();
        }
    }
    // off-chain testing by using AI api
    // data buyer input data CID, data type, description and the secret key for the dataset
    // use python bard api to evaluate the data with its description.
    function evaluateData() public payable {
        //should wait the setSimilarityScore to execute this, this is contrtolled by the off chain python code
        // this should be the offchain python function return by using ai

        if (similarityScore > 70) {
            //data seller is correct;
            //data buyer will be Forfeiture of security deposit and pay for the cost of evaluation
            payable(dataSeller).transfer(dataProductPrice);
            DataProduct(dataProductAddress).returnDeposit(dataIPFSCID);
        } else {
            //data buyer is correct;
            // data seller will be Forfeiture of security deposit and pay for the cost of evaluation
            payable(dataBuyer).transfer(dataProductPrice);
            withdrawDeposit();
        }

        // For simplicity, this is a placeholder.
        // Return true if data is considered correct, false otherwise.
    }

    // obtain the similarity_score from the python code.
    // use hundred mark system
    function setSimilarityScore(uint256 score) public onlyDataBuyer {
        // DataBuyer can set similarity score only if called by DataBuyer
        similarityScore = score;
        emit UploadScore(similarityScore);
    }

    //return the deposit for data buyer
    function withdrawDeposit() private {
        //require(isDataReceived, "Data has not been received yet.");
        //require(!isDataCorrect, "Data is incorrect, withdrawal not allowed.");
        // Calculate the amount to be refunded
        uint256 refundAmount = dataDeposit;
        // Reset contract state
        isDataReceived = false;
        isDataCorrect = false;
        isDataPaid = false;

        // Transfer the deposit back
        payable(dataBuyer).transfer(refundAmount);
    }
}

