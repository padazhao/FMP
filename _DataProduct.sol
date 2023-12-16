
// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

contract DataProduct {
    //set the data product information
    struct DataProductInfor {
        address owner; // the data product owner address
        string dataType; //give the type of data: video, img, voice, Time series
        string dataDescription; //give a description for the data content
        //string dataOrigin;//give the data origin
        //string applyAITask;//give the target ai tasks, if not idea can enter no
        string ipfsCID; // the data stored CID in ipfs;
        string sampleData; //give a sample data to display the data strucure that can set no to stand no sample
        uint256 price; // this price use eth and use same price as the deposit
    }
    address public owner;
    // key - value
    mapping(string => DataProductInfor) public dataProducts;
    string[] public productKeys; // Keep track of keys
    // notify the data state
    event DataPaid(string ipfsCID, address dataBuyer, uint256 price);

    // set yhe initial construct
    constructor() {
        owner = msg.sender;
    }

    //Restricts only the owner of the contract to perform specific operations, increasing the security and control of the contract
    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Only the owner can perform this operation"
        );
        _;
    }

    function uploadDataProduct(
        string memory _dataType,
        string memory _dataDescription,
        //string memory _dataOrigin,
        //string memory _applyAITask,
        string memory _ipfsCID,
        string memory _sampleData,
        uint256 _price//1e18
    ) external payable {
        require(bytes(_ipfsCID).length > 0, "IPFS hash cannot be empty");
        require(
            bytes(dataProducts[_ipfsCID].dataDescription).length == 0,
            "Data hash already exists"
        );
        require(
            msg.value == _price,
            "Deposit amount must match the specified price"
        );
        DataProductInfor memory newProduct = DataProductInfor({
            owner: msg.sender,
            dataType: _dataType,
            dataDescription: _dataDescription,
            //dataOrigin: _dataOrigin,
            // applyAITask: _applyAITask,
            ipfsCID: _ipfsCID,
            sampleData: _sampleData,
            price: _price
        });
        dataProducts[_ipfsCID] = newProduct;
        productKeys.push(_ipfsCID); // Add the key to the array
    }

    //obtain the data product information over ipfsCID
    function getProductDetails(string memory ipfsCID)
        public
        view
        returns (
            address,
            string memory,
            string memory,
            string memory,
            string memory,
            uint256
        )
    {
        DataProductInfor memory product = dataProducts[ipfsCID];
        require(bytes(product.dataType).length > 0, "Data hash not found");

        return (
            product.owner,
            product.dataType,
            product.dataDescription,
            product.ipfsCID,
            product.sampleData,
            product.price
        );
    }

    function getAllDataProducts()
        public
        view
        returns (
            string[] memory,
            address[] memory,
            string[] memory,
            string[] memory,
            string[] memory,
            uint256[] memory
        )
    {
        uint256 totalProducts = productKeys.length;

        string[] memory ipfsCIDs = new string[](totalProducts);
        address[] memory owners = new address[](totalProducts);
        string[] memory dataTypes = new string[](totalProducts);
        string[] memory dataDescriptions = new string[](totalProducts);
        string[] memory sampleDatas = new string[](totalProducts);
        uint256[] memory prices = new uint256[](totalProducts);

        for (uint256 i = 0; i < totalProducts; i++) {
            DataProductInfor memory product = dataProducts[productKeys[i]];

            ipfsCIDs[i] = product.ipfsCID;
            owners[i] = product.owner;
            dataTypes[i] = product.dataType;
            dataDescriptions[i] = product.dataDescription;
            sampleDatas[i] = product.sampleData;
            prices[i] = product.price;
        }

        return (
            ipfsCIDs,
            owners,
            dataTypes,
            dataDescriptions,
            sampleDatas,
            prices
        );
    }

    // Add this function to DataProduct contract
    function getProductOwner(string memory ipfsCID)
        public
        view
        returns (address)
    {
        DataProductInfor storage product = dataProducts[ipfsCID];
        require(bytes(product.dataType).length > 0, "Data hash not found");
        return product.owner;
    }
    //return deposit
    function returnDeposit(string memory ipfsCID) external {
        DataProductInfor storage product = dataProducts[ipfsCID];
        // require(
        //     msg.sender == product.owner,
        //     "Only the data product owner can return the deposit"
        // );
        // require(product.price > 0, "Product price must be greater than zero");
        // require(
        //     product.price == address(this).balance,
        //     "Deposit has not been paid for the product"
        // );

        // Transfer the deposit back to the data product owner
        payable(product.owner).transfer(product.price);

        // Reset data product state
        delete dataProducts[ipfsCID];
        for (uint256 i = 0; i < productKeys.length; i++) {
            if (keccak256(bytes(productKeys[i])) == keccak256(bytes(ipfsCID))) {
                delete productKeys[i];
                break;
            }
        }
    }

    
}
