# http://python.net/crew/theller/ctypes/reference.html
# http://python.net/crew/theller/ctypes/tutorial.html
# http://developer.apple.com/library/mac/#qa/qa1462/_index.html
# http://opensource.apple.com/source/DSTools/DSTools-162/dsenableroot/dsenableroot.cpp
# https://developer.apple.com/library/mac/#documentation/Networking/Reference/Open_Directory_Ref/Reference/reference.html
# https://developer.apple.com/library/mac/#documentation/Networking/Conceptual/Open_Directory/Introduction/Introduction.html

# Ok, starting from scratch and declaring all the types:
from ctypes import *
from ctypes.util import find_library

# libc  = CDLL(find_library('c'))
libDS = CDLL(find_library('DirectoryService'))

class tDataBuffer(Structure):
    _fields_ = [
        ('fBufferSize', c_uint32),
        ('fBufferLength', c_uint32),
        ('fBufferData', c_char * 1)]

class tDataNode(tDataBuffer):
    pass

class tDataList(Structure):
    _fields_ = [
        ('fDataNodeCount', c_uint32),
        ('fDataListHead', POINTER(tDataNode))]

class tAccessControlEntry(Structure):
    _fields_ = [
        ('fGuestAccessFlags', c_uint32),
        ('fDirMemberFlags', c_uint32),
        ('fDirNodeMemberFlags', c_uint32),
        ('fOwnerFlags', c_uint32),
        ('fAdministratorFlags', c_uint32)]

class tRecordEntry(Structure):
    _fields_ = [
        ('fReserved1', c_uint32),
        ('fReserved2', tAccessControlEntry),
        ('fRecordAttributeCount', c_uint32),
        ('fRecordNameAndType', tDataNode)]

class tAttributeEntry(Structure):
    _fields_ = [
        ('fReserved1', c_uint32),
        ('fReserved2', tAccessControlEntry),
        ('fAttributeValueCount', c_uint32),
        ('fAttributeDataSize', c_uint32),
        ('fAttributeValueMaxSize', c_uint32),
        ('fAttributeSignature', tDataNode)]

class tAttributeValueEntry(Structure):
    _fields_ = [
        ('fAttributeValueID', c_uint32),
        ('fAttributeValueData', tDataNode)]

def get_DataNode_buffer(dn_obj):
    # Doing pointer math here as the tDataNode struct only has a single char value (to python)
    recast_obj = cast(addressof(dn_obj), POINTER(tDataNode))
    return cast(addressof(recast_obj.contents) + tDataNode.fBufferData.offset, POINTER(c_char*(recast_obj.contents.fBufferLength))).contents[:]

# dsOpenDirService = libDS.dsOpenDirService
# dsFindDirNodes = libDS.dsFindDirNodes
# dsGetDirNodeName = libDS.dsGetDirNodeName
# dsDataBufferDeAllocate = libDS.dsDataBufferDeAllocate
# dsDataListDeallocate = libDS.dsDataListDeallocate
# dsOpenDirNode = libDS.dsOpenDirNode
# dsGetRecordList = libDS.dsGetRecordList
# dsGetRecordEntry = libDS.dsGetRecordEntry
# dsGetAttributeEntry = libDS.dsGetAttributeEntry
# dsGetAttributeValue = libDS.dsGetAttributeValue

# dsCloseDirService = libDS.dsCloseDirService
# dsCloseDirNode = libDS.dsCloseDirService
# dsCloseAttributeList = libDS.dsCloseAttributeList
# dsCloseAttributeValueList = libDS.dsCloseAttributeValueList
# dsDeallocRecordEntry = libDS.dsDeallocRecordEntry
# dsDeallocAttributeEntry = libDS.dsDeallocAttributeEntry
# dsDeallocAttributeValueEntry = libDS.dsDeallocAttributeValueEntry

# dsDoAttributeValueSearchWithData = libDS.dsDoAttributeValueSearchWithData

dsDataBufferAllocate = libDS.dsDataBufferAllocate
dsDataBufferAllocate.restype = POINTER(tDataBuffer)
dsBuildListFromStrings = libDS.dsBuildListFromStrings
dsBuildListFromStrings.restype = POINTER(tDataList)

eDSAuthenticationSearchNodeName = 8705
eDSiExact = 8449

dirRef = c_uint32(0)
# print "<Connecting to DS>"
status = libDS.dsOpenDirService(byref(dirRef))
# if (status == 0):
# print "<Connected.>"
dataBuff = dsDataBufferAllocate(dirRef, 2*1024);
numResults, context = c_uint32(0), c_uint32(0)
# print "<Finding Search node>"
status = libDS.dsFindDirNodes(dirRef, dataBuff, None, eDSAuthenticationSearchNodeName, byref(numResults), byref(context))
# print "<Result code: %s - # of Results: %s>" % (status, numResults)
# print "<Getting node name>"
nodePath = POINTER(tDataList)()
status = libDS.dsGetDirNodeName(dirRef, dataBuff, 1, byref(nodePath))
# print "<Result code: %s>" % status
#
# We can clear the buffer here, and should, because now we have nodePath to work from
#
_ = libDS.dsDataBufferDeAllocate(dirRef, dataBuff)
dataBuff = None
dataBuff = dsDataBufferAllocate(dirRef, 8*1024)
# tDirNodeReference             nodeRef;
# typedef   UInt32  tDirNodeReference;
nodeRef = c_uint32(0)
status = libDS.dsOpenDirNode(dirRef, nodePath, byref(nodeRef))
recName = dsBuildListFromStrings(dirRef, "mike", None)
recType = dsBuildListFromStrings(dirRef, "dsRecTypeStandard:Users", None)
attrTypes = dsBuildListFromStrings(dirRef, "dsAttributesAll", None)
#
# When you no longer need the data list, call dsDataListDeallocate to release the memory associated with it.
# When you no longer wor with the node, close it with dsCloseDirNode
#
numResults = c_uint32(0)
context = c_uint32(0)
# status = dsDoAttributeValueSearchWithData(nodeRef, dataBuff, byref(recordTypesToSearchFor), matchType, eDSContains, patternToMatch, requestedAttributes, 0, byref(numResults), byref(context))
status = libDS.dsGetRecordList(nodeRef, dataBuff, recName, eDSiExact, recType, attrTypes, 0, byref(numResults), byref(context))
status = libDS.dsDataListDeallocate(dirRef, recName)
status = libDS.dsDataListDeallocate(dirRef, recType)
status = libDS.dsDataListDeallocate(dirRef, attrTypes)

# buffer contains list of records - needs to be cleaned up when done with it

# Get record 1
attrListRef = c_uint32(0)
recordEntryPtr = POINTER(tRecordEntry)()
status = libDS.dsGetRecordEntry(nodeRef, dataBuff, c_uint32(1), byref(attrListRef), byref(recordEntryPtr))

# dataBuff was only read from previous dsGetRecordList - no changes
# Use dsCloseAttributeList when you're done accessing the attributes on the record
# Use dsDeallocRecordEntry when you're all done looking at the attributes on the record

# Get attribute 1
outAttributeValueListRef = c_uint32(0)
outAttributeInfoPtr = POINTER(tAttributeEntry)()
status = libDS.dsGetAttributeEntry(nodeRef, dataBuff, attrListRef, c_uint32(1), byref(outAttributeValueListRef), byref(outAttributeInfoPtr))

# dataBuff was only read from previous dsGetRecordList - no changes
# Use dsCloseAttributeValueList when you're done accessing the values of the attribute on the record
# Use dsDeallocAttributeEntry when you're done accessing the information on the attribute on the record

# Get value 1 of attribute 1
outAttributeValue = POINTER(tAttributeValueEntry)()
status = libDS.dsGetAttributeValue(nodeRef, dataBuff, c_uint32(1), outAttributeValueListRef, byref(outAttributeValue))

# dataBuff was only read from previous dsGetRecordList - no changes
# Use dsCloseAttributeValueList when you're done accessing the values of the attribute on the record (listed above)
# Use dsDeallocAttributeValueEntry when you're done access the value on the attribute on the record

def ds_user_exists(username):
    dirRef = c_uint32(0)
    # Connect to DS
    status = libDS.dsOpenDirService(byref(dirRef))
    if status != 0:
        return -1
    
    dataBuff = dsDataBufferAllocate(dirRef, 2*1024);
    numResults = c_uint32(0)
    context = c_uint32(0)
    # Find the authentication search node
    status = libDS.dsFindDirNodes(dirRef, dataBuff, None, eDSAuthenticationSearchNodeName, byref(numResults), byref(context))
    if (status != 0) or (numResults.value != 1L):
        return -2
    
    nodePath = POINTER(tDataList)()
    # Get the authentication search node name
    status = libDS.dsGetDirNodeName(dirRef, dataBuff, 1, byref(nodePath))
    if status != 0:
        return -3
    
    # Clean up old buffer, make a new one
    _ = libDS.dsDataBufferDeAllocate(dirRef, dataBuff)
    
    nodeRef = c_uint32(0)
    # Open the search node
    status = libDS.dsOpenDirNode(dirRef, nodePath, byref(nodeRef))
    if status != 0:
        return -4
    
    # Build search terms
    recName = dsBuildListFromStrings(dirRef, username, None)
    recType = dsBuildListFromStrings(dirRef, "dsRecTypeStandard:Users", None)
    attrTypes = dsBuildListFromStrings(dirRef, "dsAttributesAll", None)
    
    numResults = c_uint32(0)
    context = c_uint32(0)
    dataBuff = None
    dataBuff = dsDataBufferAllocate(dirRef, 8*1024)
    # Perform user object lookup
    status = libDS.dsGetRecordList(nodeRef, dataBuff, recName, eDSiExact, recType, attrTypes, 0, byref(numResults), byref(context))
    if status != 0:
        return -5
    
    # Cleanup
    status = libDS.dsDataListDeallocate(dirRef, recName)
    status = libDS.dsDataListDeallocate(dirRef, recType)
    status = libDS.dsDataListDeallocate(dirRef, attrTypes)
    _ = libDS.dsDataBufferDeAllocate(dirRef, dataBuff)
    libDS.dsCloseDirNode(nodeRef)
    libDS.dsCloseDirService(dirRef)
    # 1 or more = account exists
    return int(numResults.value)
